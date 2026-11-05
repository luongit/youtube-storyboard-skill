"""
Ghép ảnh storyboard dạng lưới cho 1 cảnh từ ảnh từng panel + caption tiếng Việt.

    python compose_storyboard.py --project projects/<slug> --scene 3 [--out path.png]

- Lưới: 4 → 2x2, 5–6 → 3x2, 7–9 → 3x3 (tự động).
- Góc trên trái mỗi ô: số thứ tự + mốc thời gian.
- Dải trắng dưới mỗi ô: HÀNH ĐỘNG (đen) / THOẠI – NHÂN VẬT (đỏ) / LỜI DẪN (xám).
- Ảnh panel lấy từ panels[].image trong script.json hoặc 05_storyboard/canh_NN/panel_XX.png.
  Thiếu ảnh → vẽ ô giữ chỗ.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

BLACK = (20, 20, 20)
RED = (210, 20, 30)
GRAY = (95, 95, 95)
WHITE = (255, 255, 255)
PAGE = (236, 236, 236)
BORDER = (30, 30, 30)

FONT_CANDIDATES = {
    "regular": ["C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/segoeui.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/System/Library/Fonts/Supplemental/Arial.ttf"],
    "bold": ["C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/segoeuib.ttf",
             "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"],
}


def font(kind: str, size: int) -> ImageFont.FreeTypeFont:
    for p in FONT_CANDIDATES[kind]:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default(size)


def fmt_t(sec: float) -> str:
    sec = float(sec)
    m = int(sec // 60)
    s = sec - 60 * m
    return f"{m}:{int(round(s)):02d}" if abs(s - round(s)) < 1e-6 else f"{m}:{s:04.1f}"


def wrap(draw: ImageDraw.ImageDraw, text: str, fnt, max_w: int) -> list[str]:
    words, lines, cur = text.split(), [], ""
    for w in words:
        test = f"{cur} {w}".strip()
        if draw.textlength(test, font=fnt) <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines or [""]


def grid_for(n: int) -> tuple[int, int]:
    if n == 1:
        return 1, 1
    if n == 2:
        return 2, 1
    if n == 3:
        return 3, 1
    if n == 4:
        return 2, 2
    if n <= 6:
        return 3, 2
    return 3, (n + 2) // 3


def caption_items(panel: dict, chars: dict) -> list[tuple[str, tuple, str]]:
    """Trả về [(nhãn, màu, nội dung)]."""
    shot = panel.get("shot", "").strip()
    action = panel.get("action_vi", "").strip()
    items = [("HÀNH ĐỘNG: ", BLACK, f"{shot} – {action}" if shot else action)]
    has_dialogue = False
    narr = []
    for line in panel.get("lines") or []:
        ch = chars.get(line.get("speaker"), {})
        text = str(line.get("text", "")).strip().strip('"“”')
        if ch.get("role") == "Lời dẫn" or line.get("speaker") == "NARRATOR":
            narr.append(("LỜI DẪN: ", GRAY, f"“{text}”"))
        else:
            has_dialogue = True
            name = ch.get("name", line.get("speaker", "")).upper()
            items.append((f"THOẠI – {name}: ", RED, f"“{text}”"))
    if not has_dialogue:
        items.append(("THOẠI: ", RED, "Không thoại"))
    return items + narr


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--scene", type=int, required=True)
    ap.add_argument("--out", default=None)
    ap.add_argument("--width", type=int, default=2400, help="Chiều rộng ảnh xuất (px)")
    args = ap.parse_args()

    project = Path(args.project).resolve()
    data = json.loads((project / "script.json").read_text(encoding="utf-8"))
    chars = {c["id"]: c for c in data.get("characters", [])}
    scene = next((s for s in data["scenes"] if int(s["scene"]) == args.scene), None)
    if scene is None:
        raise SystemExit(f"Không có cảnh {args.scene}")
    panels = sorted(scene.get("panels", []), key=lambda p: p.get("start", 0))
    n = len(panels)
    cols, rows = grid_for(n)

    W = args.width
    margin, gap = 40, 28
    cell_w = (W - 2 * margin - (cols - 1) * gap) // cols
    img_h = cell_w * 9 // 16
    pad = 16
    f_title = font("bold", 46)
    f_sub = font("regular", 28)
    f_num = font("bold", max(26, cell_w // 22))
    f_label = font("bold", max(20, cell_w // 34))
    f_text = font("regular", max(20, cell_w // 34))
    line_h = int(f_text.size * 1.32)

    tmp = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    # tính chiều cao caption cho từng panel
    cap_lines = []
    for p in panels:
        blocks = []
        for label, color, text in caption_items(p, chars):
            label_w = tmp.textlength(label, font=f_label)
            first = wrap(tmp, text, f_text, int(cell_w - 2 * pad - label_w))
            rest_text = " ".join(text.split()[len(" ".join(first[:1]).split()):])
            lines = [first[0]] + (wrap(tmp, rest_text, f_text, cell_w - 2 * pad) if rest_text else [])
            blocks.append((label, color, lines))
        cap_lines.append(blocks)
    cap_h = [pad * 2 + sum(len(b[2]) for b in blocks) * line_h + (len(blocks) - 1) * 6 for blocks in cap_lines]
    row_cap_h = [max(cap_h[r * cols:(r + 1) * cols] or [0]) for r in range(rows)]

    header_h = 120
    H = header_h + margin + sum(img_h + ch for ch in row_cap_h) + (rows - 1) * gap + margin
    page = Image.new("RGB", (W, H), PAGE)
    d = ImageDraw.Draw(page)

    title = f"CẢNH {scene['scene']} — {scene.get('title', '').upper()}"
    d.text((margin, 28), title, font=f_title, fill=BLACK)
    scene_dur = float(scene.get("duration_sec", scene.get("duration", data.get("scene_duration_sec", 10))))
    sub = f"Thời lượng: {scene_dur:.1f} giây  ·  {n} panel  ·  Cảm xúc: {scene.get('mood', '—')}"
    d.text((margin, 82), sub, font=f_sub, fill=GRAY)

    y = header_h + margin
    for r in range(rows):
        for c in range(cols):
            i = r * cols + c
            if i >= n:
                continue
            p = panels[i]
            x = margin + c * (cell_w + gap)
            # ảnh: dùng centering=(0.5, 0.15) để ưu tiên giữ nguyên phần đỉnh đầu/vương miện nhân vật
            img_rel = p.get("image") or f"05_storyboard/canh_{args.scene:02d}/panel_{int(p['panel']):02d}.png"
            img_path = project / img_rel
            if img_path.exists():
                im = ImageOps.fit(Image.open(img_path).convert("RGB"), (cell_w, img_h), Image.LANCZOS, centering=(0.5, 0.15))
            else:
                im = Image.new("RGB", (cell_w, img_h), (200, 200, 200))
                di = ImageDraw.Draw(im)
                msg = f"Chưa có ảnh panel {p['panel']}"
                di.text(((cell_w - di.textlength(msg, font=f_sub)) / 2, img_h / 2 - 16), msg, font=f_sub, fill=GRAY)
            page.paste(im, (x, y))
            # số + thời gian
            badge = f" {p['panel']} "
            tlabel = f"{fmt_t(p.get('start', 0))}–{fmt_t(p.get('end', 0))}"
            bw = d.textlength(badge, font=f_num) + 8
            bh = f_num.size + 14
            d.rectangle([x, y, x + bw, y + bh], fill=BLACK)
            d.text((x + 4, y + 5), badge, font=f_num, fill=WHITE)
            tw = d.textlength(tlabel, font=f_label) + 16
            d.rectangle([x + bw, y, x + bw + tw, y + bh], fill=(255, 255, 255))
            d.text((x + bw + 8, y + (bh - f_label.size) / 2 - 2), tlabel, font=f_label, fill=BLACK)
            # caption
            cy0 = y + img_h
            d.rectangle([x, cy0, x + cell_w, cy0 + row_cap_h[r]], fill=WHITE)
            cy = cy0 + pad
            for label, color, lines in cap_lines[i]:
                d.text((x + pad, cy), label, font=f_label, fill=color)
                lw = d.textlength(label, font=f_label)
                for li, ln in enumerate(lines):
                    d.text((x + pad + (lw if li == 0 else 0), cy), ln, font=f_text, fill=color)
                    cy += line_h
                cy += 6
            d.rectangle([x, y, x + cell_w, cy0 + row_cap_h[r]], outline=BORDER, width=3)
            d.line([x, cy0, x + cell_w, cy0], fill=BORDER, width=2)
        y += img_h + row_cap_h[r] + gap

    out = Path(args.out) if args.out else project / "05_storyboard" / f"storyboard_canh_{args.scene:02d}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    page.save(out)
    print(f"Đã lưu storyboard: {out}")


if __name__ == "__main__":
    main()
