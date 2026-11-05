import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def generate_voice_script(project_dir: Path) -> Path:
    script_path = project_dir / "script.json"
    if not script_path.exists():
        raise FileNotFoundError(f"Không tìm thấy {script_path}")

    with open(script_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    chars = {c["id"]: c.get("name", c["id"]) for c in data.get("characters", [])}
    scenes = sorted(data.get("scenes", []), key=lambda s: int(s.get("scene", 0)))

    lines_out = []
    lines_out.append(f"# voice script: {data.get('project', '').lower()}")
    lines_out.append("")
    lines_out.append("## 1. kịch bản đọc liền mạch (toàn bộ viết thường)")
    lines_out.append("")

    all_speech_texts = []
    scene_blocks = []

    for sc in scenes:
        s_num = int(sc.get("scene", 0))
        s_title = sc.get("title", "").lower()
        panels = sorted(sc.get("panels", []), key=lambda p: float(p.get("start", 0)))

        sc_lines = []
        for p in panels:
            p_num = int(p.get("panel", 0))
            for l in p.get("lines", []):
                raw_text = l.get("text", "").strip().strip('"“”')
                if not raw_text:
                    continue
                # Chuyển toàn bộ thành chữ thường (không in hoa)
                lower_text = raw_text.lower()
                all_speech_texts.append(lower_text)
                spk_id = l.get("speaker", "NARRATOR")
                spk_name = chars.get(spk_id, spk_id).lower()
                sc_lines.append((p_num, spk_name, lower_text))

        scene_blocks.append((s_num, s_title, sc_lines))

    # Phần 1: Toàn bộ văn bản nối tiếp nhau bằng chữ thường
    for text in all_speech_texts:
        lines_out.append(f"{text}")
        lines_out.append("")

    lines_out.append("---")
    lines_out.append("")
    lines_out.append("## 2. kịch bản phân vai theo từng cảnh (toàn bộ viết thường)")
    lines_out.append("")

    for s_num, s_title, sc_lines in scene_blocks:
        lines_out.append(f"### cảnh {s_num}: {s_title}")
        for p_num, spk_name, text in sc_lines:
            lines_out.append(f"- [{spk_name}] (panel {p_num}): {text}")
        lines_out.append("")

    out_file = project_dir / "voice-script.md"
    out_file.write_text("\n".join(lines_out), encoding="utf-8")
    print(f" Đã tạo thành công {out_file} (tổng {len(all_speech_texts)} câu thoại, toàn bộ viết thường).")
    return out_file

if __name__ == "__main__":
    proj = Path("outputs/Kinh_Bo_Thi_Va_Cung_Duong_Nhu_Phap")
    if len(sys.argv) > 1:
        proj = Path(sys.argv[1])
    generate_voice_script(proj)
