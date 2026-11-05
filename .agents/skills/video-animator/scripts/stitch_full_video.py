"""
Ghép tất cả các file video cảnh (canh_01.mp4 ... canh_NN.mp4) thành video hoàn chỉnh full_video.mp4.

    python stitch_full_video.py --project outputs/<project> [--out full_video.mp4]
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
    except Exception:
        pass

FFMPEG = shutil.which("ffmpeg")


def main() -> None:
    ap = argparse.ArgumentParser(description="Ghép toàn bộ video các cảnh thành video hoàn chỉnh")
    ap.add_argument("--project", required=True)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    if not FFMPEG:
        raise SystemExit("Cần có ffmpeg trong PATH.")

    project = Path(args.project).resolve()
    script_data = json.loads((project / "script.json").read_text(encoding="utf-8"))
    scenes = sorted(script_data.get("scenes", []), key=lambda s: int(s["scene"]))

    videos_dir = project / "videos"
    clip_files = []
    for s in scenes:
        n = int(s["scene"])
        p = videos_dir / f"canh_{n:02d}.mp4"
        if not p.exists():
            raise SystemExit(f"Thiếu file video: {p}")
        clip_files.append(p)

    out_mp4 = Path(args.out) if args.out else videos_dir / "full_video.mp4"
    out_mp4.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as td:
        concat_txt = Path(td) / "concat.txt"
        concat_txt.write_text(
            "\n".join([f"file '{c.as_posix()}'" for c in clip_files]),
            encoding="utf-8",
        )

        cmd = [
            FFMPEG, "-y", "-loglevel", "error",
            "-f", "concat", "-safe", "0", "-i", str(concat_txt),
            "-c", "copy",
            str(out_mp4),
        ]
        subprocess.run(cmd, check=True)
        print(f"Đã ghép thành công {len(clip_files)} cảnh thành: {out_mp4}")


if __name__ == "__main__":
    main()
