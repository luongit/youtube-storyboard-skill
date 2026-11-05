"""
Kiểm tra script.json theo quy tắc của skill storyboard-director.

    python validate_script.py --project projects/<slug>

Mã thoát 1 nếu có ERROR.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

WORDS_PER_SEC = 3.3          # tốc độ đọc tiếng Việt tự nhiên
MIN_WORDS, MAX_WORDS = 25, 35
MIN_PANELS, MAX_PANELS = 1, 8     # Linh hoạt từ 1 panel (long take) đến 8 panels (fast cut)
MAX_LINE_SEC = 3.2


def count_words(text: str) -> int:
    return len(re.findall(r"\w+", text, flags=re.UNICODE))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    args = ap.parse_args()
    path = Path(args.project) / "script.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    errors: list[str] = []
    warns: list[str] = []
    default_dur = float(data.get("scene_duration_sec", 10))
    char_ids = {c["id"] for c in data.get("characters", [])}
    loc_ids = {l["id"] for l in data.get("locations", [])}

    for c in data.get("characters", []):
        if c.get("role") != "Lời dẫn" and not c.get("anchor_en"):
            warns.append(f"Nhân vật {c['id']}: chưa có anchor_en (cần trước Giai đoạn 3).")
        if not c.get("voice"):
            warns.append(f"Nhân vật {c['id']}: chưa gán giọng (voice).")

    scenes = data.get("scenes", [])
    nums = [s.get("scene") for s in scenes]
    if nums != list(range(1, len(scenes) + 1)):
        warns.append(f"Số cảnh không liên tục: {nums}")

    print(f"{'Cảnh':>4} | {'Thời lượng':>10} | {'Panel':>5} | {'Từ':>3} | {'~Giây nói':>9} | Tiêu đề")
    print("-" * 80)
    total_project_sec = 0.0
    for sc in scenes:
        n = sc.get("scene")
        dur = float(sc.get("duration_sec", sc.get("duration", default_dur)))
        total_project_sec += dur
        panels = sorted(sc.get("panels", []), key=lambda p: p.get("start", 0))
        total_words = 0
        if not (MIN_PANELS <= len(panels) <= MAX_PANELS):
            errors.append(f"Cảnh {n}: có {len(panels)} panel (yêu cầu {MIN_PANELS}–{MAX_PANELS}).")
        if sc.get("location") and loc_ids and sc["location"] not in loc_ids:
            warns.append(f"Cảnh {n}: location '{sc['location']}' không có trong locations[].")
        prev_end = 0.0
        for p in panels:
            pid = p.get("panel")
            s, e = float(p.get("start", -1)), float(p.get("end", -1))
            if abs(s - prev_end) > 0.01:
                errors.append(f"Cảnh {n} panel {pid}: bắt đầu {s}s, không nối tiếp {prev_end}s.")
            if not (0.5 <= e - s <= dur):
                warns.append(f"Cảnh {n} panel {pid}: dài {e - s:.1f}s (chuẩn 0.5–{dur:.0f}s).")
            prev_end = e
            if not p.get("action_vi"):
                errors.append(f"Cảnh {n} panel {pid}: thiếu action_vi (mô tả hành động).")
            panel_words = 0
            for line in p.get("lines") or []:
                spk = line.get("speaker")
                if spk not in char_ids:
                    errors.append(f"Cảnh {n} panel {pid}: speaker '{spk}' không có trong characters[].")
                w = count_words(line.get("text", ""))
                panel_words += w
                total_words += w
            line_sec = panel_words / WORDS_PER_SEC
            panel_dur = e - s
            if line_sec > panel_dur + 0.3:
                warns.append(f"Cảnh {n} panel {pid}: {panel_words} từ (~{line_sec:.1f}s) "
                             f"vượt quá thời lượng panel ({panel_dur:.1f}s), nên kéo dài panel hoặc rút ngắn thoại.")
        if panels and abs(prev_end - dur) > 0.01:
            errors.append(f"Cảnh {n}: panel cuối kết thúc {prev_end}s, phải là {dur:.1f}s theo thời lượng cảnh.")
        max_words_allowed = int(round(dur * 3.6))
        if total_words > max_words_allowed:
            errors.append(f"Cảnh {n}: {total_words} từ lời nói quá dài so với thời lượng {dur:.1f}s (tối đa ~{max_words_allowed} từ).")
        print(f"{n:>4} | {dur:>9.1f}s | {len(panels):>5} | {total_words:>3} | {total_words / WORDS_PER_SEC:>9.1f} | {sc.get('title', '')}")

    print()
    for w in warns:
        print(f"WARN : {w}")
    for e in errors:
        print(f"ERROR: {e}")
    print(f"\nKết quả: {len(errors)} lỗi, {len(warns)} cảnh báo, {len(scenes)} cảnh "
          f"(tổng {total_project_sec:.1f}s).")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
