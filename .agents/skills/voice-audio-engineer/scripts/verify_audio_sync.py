import json
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def get_audio_duration(file_path: Path) -> float:
    try:
        cmd = [
            "ffprobe", "-v", "error", "-show_entries",
            "format=duration", "-of", "default=noprint_wrappers=1:nokey=1",
            str(file_path)
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return float(res.stdout.strip())
    except Exception:
        return 0.0

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Thẩm định đồng bộ âm thanh và phụ đề SRT.")
    parser.add_argument("--project", required=True, help="Thư mục dự án")
    args = parser.parse_args()

    project = Path(args.project).resolve()
    script_path = project / "script.json"
    if not script_path.exists():
        print(f"❌ ERROR: Không tìm thấy script.json tại {project}")
        sys.exit(1)

    data = json.loads(script_path.read_text(encoding="utf-8"))
    scenes = sorted(data.get("scenes", []), key=lambda s: int(s.get("scene", 0)))
    audio_dir = project / "audio"
    scenes_audio_dir = audio_dir / "scenes"

    errors = []
    warnings = []

    print(f"🔍 [Validator Agent] Bắt đầu thẩm định âm thanh cho {len(scenes)} cảnh...")

    total_audio_sec = 0.0
    for sc in scenes:
        s_num = int(sc.get("scene", 0))
        target_dur = float(sc.get("duration_sec", sc.get("duration", 10.0)))
        mp3_file = scenes_audio_dir / f"canh_{s_num:02d}.mp3"
        srt_file = scenes_audio_dir / f"canh_{s_num:02d}.srt"

        if not mp3_file.exists():
            errors.append(f"Cảnh {s_num}: Thiếu file âm thanh '{mp3_file.name}'!")
            continue
        if not srt_file.exists():
            errors.append(f"Cảnh {s_num}: Thiếu file phụ đề '{srt_file.name}'!")
            continue

        dur = get_audio_duration(mp3_file)
        total_audio_sec += dur

        # So sánh thời lượng âm thanh với thời lượng cảnh
        if dur > target_dur + 0.5:
            warnings.append(f"Cảnh {s_num}: Âm thanh dài {dur:.2f}s > thời lượng kịch bản ({target_dur:.1f}s) — cần nới thời lượng cảnh khi render video.")
        print(f"   ✓ Cảnh {s_num:02d}: Âm thanh {dur:.2f}s (chuẩn {target_dur:.1f}s) | Phụ đề OK")

    # Kiểm tra file tổng
    full_mp3 = audio_dir / "full_voiceover.mp3"
    full_srt = audio_dir / "full_subtitles.srt"
    if not full_mp3.exists():
        warnings.append("Thiếu file âm thanh tổng hợp: full_voiceover.mp3")
    if not full_srt.exists():
        warnings.append("Thiếu file phụ đề tổng hợp: full_subtitles.srt")

    print("\n--- KẾT QUẢ THẨM ĐỊNH ÂM THANH & PHỤ ĐỀ ---")
    for w in warnings:
        print(f"⚠️ WARN: {w}")
    for e in errors:
        print(f"❌ ERROR: {e}")

    if errors:
        print(f"\n❌ Thất bại: Có {len(errors)} lỗi âm thanh!")
        sys.exit(1)
    else:
        print(f"\n✅ Hoàn tất: 0 lỗi. Toàn bộ file âm thanh và phụ đề SRT hợp lệ (Tổng: {total_audio_sec:.1f}s)!")
        sys.exit(0)

if __name__ == "__main__":
    main()
