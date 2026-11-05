"""
Tạo video animatic chuyển động (Ken Burns / Pan & Zoom) từ các panel storyboard và âm thanh MP3.

    python render_scene_video.py --project outputs/<project> --scene 1 [--out output.mp4]

- Sử dụng FFmpeg tạo chuyển động máy quay điện ảnh (push-in, pan, tracking) cho từng panel.
- Ghép với file âm thanh cảnh (canh_NN.mp3).
- Xuất video chuẩn Full HD 1080p (1920x1080), 30fps H.264.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

FFMPEG = shutil.which("ffmpeg")


def get_camera_filter(motion: str, dur: float, fps: int, w: int, h: int) -> str:
    """Tạo bộ lọc FFmpeg zoompan tương ứng với chuyển động máy quay.
    ĐẶC BIỆT LƯU Ý: Giữ an toàn vùng đỉnh (headroom) bằng cách neo trục Y sát đỉnh
    y='max(0, (ih-ih/zoom)*0.15)' để KHÔNG BAO GIỜ bị cắt mất đầu/búi tóc/vương miện nhân vật.
    """
    n_frames = max(1, int(round(dur * fps)))
    m = (motion or "").lower().strip()
    # Y an toàn giữ trọn vẹn đầu nhân vật: neo tỷ lệ cắt đỉnh tối đa chỉ ~15% của phần zoom
    y_safe = "max(0,(ih-ih/zoom)*0.15)"
    
    if "fast_push" in m or "fast push" in m or "dramatic" in m:
        # Zoom nhanh cận cảnh biểu cảm (neo Y an toàn tránh mất đầu)
        return f"zoompan=z='min(zoom+0.0035,1.25)':d={n_frames}:x='iw/2-(iw/zoom/2)':y='{y_safe}':s={w}x{h}:fps={fps}"
    elif "pull" in m:
        # Thu máy lùi dần hé lộ bối cảnh
        rate = 0.16 / n_frames
        return f"zoompan=z='max(1.16-{rate:.6f}*on,1.0)':d={n_frames}:x='iw/2-(iw/zoom/2)':y='{y_safe}':s={w}x{h}:fps={fps}"
    elif "pan_left" in m or "pan left" in m:
        # Lia máy từ phải sang trái
        return f"zoompan=z='1.10':d={n_frames}:x='if(lte(on,1),(iw-iw/zoom)*0.75,max(x-0.8,(iw-iw/zoom)*0.25))':y='{y_safe}':s={w}x{h}:fps={fps}"
    elif "pan_right" in m or "pan right" in m or "pan" in m:
        # Lia máy chậm từ trái sang phải
        return f"zoompan=z='1.10':d={n_frames}:x='if(lte(on,1),(iw-iw/zoom)*0.25,min(x+0.8,(iw-iw/zoom)*0.75))':y='{y_safe}':s={w}x{h}:fps={fps}"
    elif "static" in m:
        # Máy quay tĩnh
        return f"zoompan=z='1.0':d={n_frames}:x='iw/2-(iw/zoom/2)':y='0':s={w}x{h}:fps={fps}"
    else:
        # Mặc định: zoom in nhẹ nhàng vào trung tâm theo thời lượng thực tế (giữ trọn vẹn đầu)
        rate = 0.14 / n_frames
        return f"zoompan=z='min(zoom+{rate:.6f},1.15)':d={n_frames}:x='iw/2-(iw/zoom/2)':y='{y_safe}':s={w}x{h}:fps={fps}"


def main() -> None:
    ap = argparse.ArgumentParser(description="Render video animatic cho cảnh storyboard")
    ap.add_argument("--project", required=True)
    ap.add_argument("--scene", type=int, required=True)
    ap.add_argument("--out", default=None)
    ap.add_argument("--letterbox", action="store_true", help="Thêm 2 dải đen điện ảnh 2.35:1 Cinematic scope")
    args = ap.parse_args()

    if not FFMPEG:
        raise SystemExit("Cần có ffmpeg trong PATH.")

    project = Path(args.project).resolve()
    script_data = json.loads((project / "script.json").read_text(encoding="utf-8"))
    scene = next((s for s in script_data["scenes"] if int(s["scene"]) == args.scene), None)
    if not scene:
        raise SystemExit(f"Không tìm thấy cảnh {args.scene}")

    panels_dir = project / "05_storyboard" / f"canh_{args.scene:02d}"
    audio_path = project / "audio" / "scenes" / f"canh_{args.scene:02d}.mp3"

    if not panels_dir.exists():
        raise SystemExit(f"Chưa có thư mục panel ảnh: {panels_dir}")

    out_mp4 = Path(args.out) if args.out else project / "videos" / f"canh_{args.scene:02d}.mp4"
    out_mp4.parent.mkdir(parents=True, exist_ok=True)

    fps = 30
    w, h = 1920, 1080
    panels = sorted(scene.get("panels", []), key=lambda p: p.get("start", 0))

    # Tự động chọn motion nếu panel chưa chỉ định rõ
    default_motions = ["slow_push_in", "slow_pan_right", "fast_push_in", "slow_pull_out"]

    with tempfile.TemporaryDirectory() as td:
        tmp_dir = Path(td)
        clip_files = []

        for idx, p in enumerate(panels):
            pid = int(p.get("panel", idx + 1))
            dur = float(p.get("end", 2.5)) - float(p.get("start", 0.0))
            dur = max(0.5, dur)

            img_path = panels_dir / f"panel_{pid:02d}.png"
            if not img_path.exists():
                img_path = panels_dir / f"panel_{pid:02d}.jpg"
            if not img_path.exists():
                raise SystemExit(f"Thiếu file ảnh: {img_path}")

            clip_mp4 = tmp_dir / f"clip_{pid:02d}.mp4"
            
            # Đọc camera motion từ kịch bản hoặc chọn mặc định theo shot
            shot_str = p.get("shot", "").lower()
            panel_motion = p.get("camera_motion", "")
            if not panel_motion:
                if "cận" in shot_str or "đặc tả" in shot_str:
                    panel_motion = "fast_push_in" if "nhanh" in p.get("action_vi", "").lower() else "slow_push_in"
                elif "toàn cảnh" in shot_str or "viễn cảnh" in shot_str:
                    panel_motion = "slow_pan_right"
                else:
                    panel_motion = default_motions[idx % len(default_motions)]

            vf = get_camera_filter(panel_motion, dur, fps, w, h)
            filters = [f"scale=2560:-1", vf]
            if args.letterbox:
                # Dải đen điện ảnh 2.35:1 Cinematic scope (120px trên dưới)
                filters.append("drawbox=y=0:h=120:color=black:t=fill")
                filters.append("drawbox=y=ih-120:h=120:color=black:t=fill")
            filters.append("format=yuv420p")
            vf_str = ",".join(filters)

            cmd = [
                FFMPEG, "-y", "-loglevel", "error",
                "-loop", "1", "-i", str(img_path),
                "-vf", vf_str,
                "-t", f"{dur:.3f}",
                "-c:v", "libx264", "-preset", "fast", "-crf", "18",
                str(clip_mp4),
            ]
            subprocess.run(cmd, check=True)
            clip_files.append(clip_mp4)

        # Tạo file danh sách nối
        concat_txt = tmp_dir / "concat.txt"
        concat_txt.write_text(
            "\n".join([f"file '{c.as_posix()}'" for c in clip_files]),
            encoding="utf-8",
        )

        video_no_audio = tmp_dir / "video_no_audio.mp4"
        subprocess.run(
            [
                FFMPEG, "-y", "-loglevel", "error",
                "-f", "concat", "-safe", "0", "-i", str(concat_txt),
                "-c", "copy",
                str(video_no_audio),
            ],
            check=True,
        )

        # Ghép audio (nếu có)
        if audio_path.exists():
            cmd_final = [
                FFMPEG, "-y", "-loglevel", "error",
                "-i", str(video_no_audio),
                "-i", str(audio_path),
                "-c:v", "copy",
                "-c:a", "aac", "-b:a", "192k",
                "-shortest",
                str(out_mp4),
            ]
        else:
            cmd_final = [
                FFMPEG, "-y", "-loglevel", "error",
                "-i", str(video_no_audio),
                "-c", "copy",
                str(out_mp4),
            ]

        subprocess.run(cmd_final, check=True)
        print(f"Đã render video animatic thành công: {out_mp4}")


if __name__ == "__main__":
    main()
