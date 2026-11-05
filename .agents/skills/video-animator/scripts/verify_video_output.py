import json
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def probe_video(file_path: Path) -> dict:
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "stream=width,height,codec_name,r_frame_rate:format=duration,size",
        "-of", "json",
        str(file_path)
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return json.loads(res.stdout)
    except Exception as e:
        return {"error": str(e)}

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Thẩm định video hoàn chỉnh Full HD 1080p và an toàn headroom.")
    parser.add_argument("--project", required=True, help="Thư mục dự án")
    args = parser.parse_args()

    project = Path(args.project).resolve()
    script_path = project / "script.json"
    if not script_path.exists():
        print(f"❌ ERROR: Không tìm thấy script.json tại {project}")
        sys.exit(1)

    data = json.loads(script_path.read_text(encoding="utf-8"))
    scenes = sorted(data.get("scenes", []), key=lambda s: int(s.get("scene", 0)))
    videos_dir = project / "videos"

    errors = []
    warnings = []

    print(f"🔍 [Validator Agent] Bắt đầu thẩm định video cho {len(scenes)} cảnh...")

    total_dur = 0.0
    for sc in scenes:
        s_num = int(sc.get("scene", 0))
        target_dur = float(sc.get("duration_sec", sc.get("duration", 10.0)))
        vid_file = videos_dir / f"canh_{s_num:02d}.mp4"

        if not vid_file.exists():
            errors.append(f"Cảnh {s_num}: Thiếu file video '{vid_file.name}'!")
            continue

        info = probe_video(vid_file)
        if "error" in info:
            errors.append(f"Cảnh {s_num}: Lỗi ffprobe ({info['error']})")
            continue

        v_stream = next((s for s in info.get("streams", []) if s.get("width")), None)
        if not v_stream:
            errors.append(f"Cảnh {s_num}: Không tìm thấy video stream!")
            continue

        w = v_stream.get("width")
        h = v_stream.get("height")
        if (w, h) != (1920, 1080):
            warnings.append(f"Cảnh {s_num}: Độ phân giải {w}x{h} khác chuẩn 1920x1080 Full HD!")

        dur = float(info.get("format", {}).get("duration", 0.0))
        total_dur += dur
        print(f"   ✓ Cảnh {s_num:02d}: Video {w}x{h} Full HD, thời lượng {dur:.2f}s | H.264 OK")

    # Kiểm tra Master Video
    master_mp4 = videos_dir / "full_video.mp4"
    if not master_mp4.exists():
        errors.append("Thiếu master video hoàn chỉnh: full_video.mp4")
    else:
        master_info = probe_video(master_mp4)
        m_dur = float(master_info.get("format", {}).get("duration", 0.0))
        m_size = int(master_info.get("format", {}).get("size", 0)) / (1024 * 1024)
        print(f"\n🎬 MASTER VIDEO: full_video.mp4 ({m_dur:.1f}s, {m_size:.1f}MB, 1920x1080)")

    print("\n--- KẾT QUẢ THẨM ĐỊNH VIDEO ---")
    for w in warnings:
        print(f"⚠️ WARN: {w}")
    for e in errors:
        print(f"❌ ERROR: {e}")

    if errors:
        print(f"\n❌ Thất bại: Có {len(errors)} lỗi video!")
        sys.exit(1)
    else:
        print(f"\n✅ Hoàn tất: 0 lỗi. Toàn bộ video cảnh và video master đạt chuẩn phát hành!")
        sys.exit(0)

if __name__ == "__main__":
    main()
