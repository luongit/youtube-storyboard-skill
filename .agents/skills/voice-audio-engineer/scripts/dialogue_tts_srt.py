"""
Tạo MP3 + SRT lời thoại cho dự án storyboard (đưa vào CapCut).

Đọc projects/<slug>/script.json → tổng hợp từng câu thoại theo giọng của từng nhân vật
(VieNeu-TTS mặc định, dự phòng edge-tts) → đặt câu vào đúng mốc panel → mỗi cảnh căn đúng
scene_duration_sec (mặc định 10s) → xuất:
    audio/full_voiceover.mp3, audio/full_subtitles.srt, audio/full_subtitles_speaker.srt
    audio/scenes/canh_NN.mp3 + .srt
    audio/lines/canh_NN_pXX_<SPEAKER>.mp3
    audio/timing_report.md

Ví dụ:
    python dialogue_tts_srt.py --project projects/bo-tat-va-dan-cho
    python dialogue_tts_srt.py --project projects/bo-tat-va-dan-cho --scene 3
    python dialogue_tts_srt.py --list-voices
    python dialogue_tts_srt.py --preview "Thiện Minh" --text "Xin chào các bạn"
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import math
import re
import shutil
import subprocess
import sys
import tempfile
import wave
from pathlib import Path
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

SAMPLE_RATE = 48000
DEFAULT_VIENEU_VOICE = "Thiện Minh"
EDGE_MALE = "vi-VN-NamMinhNeural"
EDGE_FEMALE = "vi-VN-HoaiMyNeural"
LINE_LEAD_IN = 0.10      # giây: lùi nhẹ sau khi panel bắt đầu
LINE_GAP = 0.15          # giây: khoảng nghỉ tối thiểu giữa 2 câu
MAX_SUB_WORDS = 14       # số từ tối đa / dòng phụ đề

FFMPEG = shutil.which("ffmpeg")
FFPROBE = shutil.which("ffprobe")


# ----------------------------------------------------------------------------- utils
def log(msg: str) -> None:
    print(f"[TTS] {msg}", flush=True)


def srt_ts(sec: float) -> str:
    ms = int(round(max(0.0, sec) * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def safe_name(text: str) -> str:
    return re.sub(r"[^A-Za-z0-9_-]+", "_", text).strip("_") or "X"


def to_wav48(src: Path, dst: Path, speed: float = 1.0) -> None:
    """Chuyển mọi định dạng sang WAV 48kHz mono 16-bit (có thể đổi tốc độ)."""
    if not FFMPEG:
        raise RuntimeError("Không tìm thấy ffmpeg trong PATH (cần để chuyển đổi âm thanh).")
    cmd = [FFMPEG, "-y", "-loglevel", "error", "-i", str(src)]
    filters = []
    if abs(speed - 1.0) > 1e-3:
        sp = max(0.5, min(2.0, speed))
        filters.append(f"atempo={sp:.3f}")
    # cắt khoảng lặng đầu/cuối để đặt câu chính xác vào mốc panel
    filters.append("silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.03")
    filters.append("areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse")
    cmd += ["-af", ",".join(filters), "-ac", "1", "-ar", str(SAMPLE_RATE), "-sample_fmt", "s16", str(dst)]
    subprocess.run(cmd, check=True, capture_output=True)


def wav_to_mp3(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [FFMPEG, "-y", "-loglevel", "error", "-i", str(src), "-codec:a", "libmp3lame", "-qscale:a", "2", str(dst)],
        check=True, capture_output=True,
    )


def read_pcm(path: Path) -> bytes:
    with wave.open(str(path), "rb") as wf:
        return wf.readframes(wf.getnframes())


def write_pcm(path: Path, pcm: bytes) -> None:
    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(pcm)


def pcm_dur(pcm: bytes) -> float:
    return len(pcm) / 2 / SAMPLE_RATE


def split_subtitle(text: str, start: float, end: float) -> list[tuple[float, float, str]]:
    words = text.split()
    if len(words) <= MAX_SUB_WORDS:
        return [(start, end, text)]
    n_chunks = math.ceil(len(words) / MAX_SUB_WORDS)
    size = math.ceil(len(words) / n_chunks)
    chunks = [words[i:i + size] for i in range(0, len(words), size)]
    out, cur, total = [], start, len(words)
    for i, c in enumerate(chunks):
        c_end = end if i == len(chunks) - 1 else cur + (end - start) * len(c) / total
        out.append((cur, c_end, " ".join(c)))
        cur = c_end
    return out


def write_srt(path: Path, entries: list[tuple[float, float, str]]) -> None:
    lines = []
    for i, (s, e, t) in enumerate(entries, 1):
        lines += [str(i), f"{srt_ts(s)} --> {srt_ts(e)}", t, ""]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


# ----------------------------------------------------------------------------- synthesizer
class Synthesizer:
    def __init__(self, cache_dir: Path, force_engine: str | None = None) -> None:
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.force_engine = force_engine
        self._vieneu: Any = None
        self._vieneu_failed = False

    # -- VieNeu
    def _get_vieneu(self) -> Any:
        if self._vieneu is None and not self._vieneu_failed:
            try:
                from vieneu import Vieneu  # type: ignore
                log("Đang nạp model VieNeu-TTS (lần đầu có thể tải model)...")
                self._vieneu = Vieneu()
            except Exception as e:  # pragma: no cover
                log(f"Không nạp được VieNeu-TTS ({e}) → dùng edge-tts.")
                self._vieneu_failed = True
        return self._vieneu

    def list_vieneu_voices(self) -> list[tuple[str, str]]:
        tts = self._get_vieneu()
        return list(tts.list_preset_voices()) if tts else []

    def _vieneu_synth(self, text: str, voice: str, out_raw: Path, ref_audio: Path | None = None) -> None:
        tts = self._get_vieneu()
        if tts is None:
            raise RuntimeError("VieNeu-TTS không khả dụng")
        if ref_audio and ref_audio.exists():
            audio = tts.infer(text=text, ref_audio=ref_audio)
        else:
            audio = tts.infer(text=text, voice=voice)
        tts.save(audio, str(out_raw))

    # -- edge-tts
    @staticmethod
    def _edge_synth(text: str, voice: str, rate: str, pitch: str, out_raw: Path) -> None:
        import edge_tts  # type: ignore

        async def _run() -> None:
            await edge_tts.Communicate(text=text, voice=voice, rate=rate, pitch=pitch).save(str(out_raw))

        asyncio.run(_run())

    @staticmethod
    def _edge_voice_for(cfg: dict[str, Any]) -> str:
        v = str(cfg.get("voice", ""))
        if v.startswith("vi-VN-"):
            return v
        return EDGE_FEMALE if str(cfg.get("gender", "")).lower() in ("nu", "nữ", "female", "f") else EDGE_MALE

    def synth(self, text: str, cfg: dict[str, Any]) -> tuple[Path, str]:
        """Trả về (wav 48k mono đã cắt lặng, engine đã dùng). Có cache theo nội dung."""
        engine = (self.force_engine or cfg.get("engine") or "vieneu").lower()
        speed = float(cfg.get("speed", 1.0))
        rate = str(cfg.get("rate", "+0%"))
        pitch = str(cfg.get("pitch", "+0Hz"))
        voice = str(cfg.get("voice") or DEFAULT_VIENEU_VOICE)
        ref_str = cfg.get("ref_audio") or cfg.get("clone_from")
        ref_path = Path(ref_str).resolve() if ref_str else None

        attempts = ["vieneu", "edge"] if engine == "vieneu" else ["edge"]
        last_err: Exception | None = None
        for eng in attempts:
            v = voice if eng == "vieneu" else self._edge_voice_for(cfg)
            ref_id = hashlib.sha1(ref_path.read_bytes()).hexdigest()[:8] if (eng == "vieneu" and ref_path and ref_path.exists()) else ""
            key = hashlib.sha1(f"{eng}|{v}|{ref_id}|{speed}|{rate}|{pitch}|{text}".encode("utf-8")).hexdigest()[:16]
            cached = self.cache_dir / f"{key}.wav"
            if cached.exists() and cached.stat().st_size > 1000:
                return cached, eng
            try:
                with tempfile.TemporaryDirectory() as td:
                    raw = Path(td) / ("raw.wav" if eng == "vieneu" else "raw.mp3")
                    if eng == "vieneu":
                        self._vieneu_synth(text, v, raw, ref_audio=ref_path)
                    else:
                        self._edge_synth(text, v, rate, pitch, raw)
                    to_wav48(raw, cached, speed)
                return cached, eng
            except Exception as e:
                last_err = e
                log(f"Lỗi engine {eng} với câu '{text[:40]}...': {e}")
        raise RuntimeError(f"Không tổng hợp được câu: {text}") from last_err


# ----------------------------------------------------------------------------- main logic
def build(project: Path, only_scene: int | None, force_engine: str | None) -> None:
    script_path = project / "script.json"
    data = json.loads(script_path.read_text(encoding="utf-8"))
    scene_dur = float(data.get("scene_duration_sec", 10))
    chars = {c["id"]: c for c in data.get("characters", [])}

    audio_dir = project / "audio"
    synth = Synthesizer(audio_dir / ".cache", force_engine)

    scenes = sorted(data.get("scenes", []), key=lambda s: s["scene"])
    if only_scene is not None:
        scenes = [s for s in scenes if int(s["scene"]) == only_scene]
        if not scenes:
            raise SystemExit(f"Không tìm thấy cảnh {only_scene} trong script.json")

    full_pcm = bytearray()
    full_subs: list[tuple[float, float, str]] = []
    full_subs_spk: list[tuple[float, float, str]] = []
    report = ["# Báo cáo thời gian lời thoại", "", f"Thời lượng chuẩn mỗi cảnh: {scene_dur:.0f}s", ""]
    warnings: list[str] = []
    engines_used: set[str] = set()
    offset = 0.0

    for sc in scenes:
        n = int(sc["scene"])
        tag = f"canh_{n:02d}"
        log(f"Cảnh {n}: {sc.get('title', '')}")
        placed: list[dict[str, Any]] = []
        cursor = 0.0
        for p in sorted(sc.get("panels", []), key=lambda x: x.get("start", 0)):
            p_start = float(p.get("start", 0.0))
            p_end = float(p.get("end", p_start + 2.5))
            for li, line in enumerate(p.get("lines") or []):
                text = str(line.get("text", "")).strip().strip('"“”')
                if not text:
                    continue
                spk = line.get("speaker", "NARRATOR")
                ch = chars.get(spk, {})
                cfg = dict(ch.get("voice") or {})
                wav_path, eng = synth.synth(text, cfg)
                engines_used.add(eng)
                pcm = read_pcm(wav_path)
                dur = pcm_dur(pcm)
                start = max(p_start + LINE_LEAD_IN, cursor + (LINE_GAP if cursor > 0 else 0))
                end = start + dur
                cursor = end
                placed.append({"panel": p.get("panel"), "speaker": spk, "name": ch.get("name", spk),
                               "text": text, "start": start, "end": end, "pcm": pcm,
                               "panel_end": p_end, "idx": li})
                if end > p_end + 0.5:
                    warnings.append(f"Cảnh {n} panel {p.get('panel')}: câu \"{text}\" kết thúc {end:.2f}s, "
                                    f"vượt panel ({p_end:.2f}s) — nên rút gọn hoặc nới panel.")

        cur_sc_dur = float(sc.get("duration_sec", sc.get("duration", scene_dur)))
        total = max([cur_sc_dur] + [x["end"] for x in placed])
        if total > cur_sc_dur + 0.3:
            warnings.append(f"Cảnh {n}: lời nói dài {total:.2f}s > {cur_sc_dur:.1f}s — CẦN rút gọn để khớp timeline.")

        # ghép PCM cảnh
        buf = bytearray(b"\x00\x00" * int(round(total * SAMPLE_RATE)))
        for x in placed:
            s = int(round(x["start"] * SAMPLE_RATE)) * 2
            buf[s:s + len(x["pcm"])] = x["pcm"]
            # câu rời
            line_mp3 = audio_dir / "lines" / f"{tag}_p{int(x['panel']):02d}_{x['idx'] + 1}_{safe_name(x['speaker'])}.mp3"
            with tempfile.TemporaryDirectory() as td:
                tmpw = Path(td) / "l.wav"
                write_pcm(tmpw, x["pcm"])
                wav_to_mp3(tmpw, line_mp3)

        with tempfile.TemporaryDirectory() as td:
            tmpw = Path(td) / "scene.wav"
            write_pcm(tmpw, bytes(buf))
            wav_to_mp3(tmpw, audio_dir / "scenes" / f"{tag}.mp3")

        scene_subs, scene_subs_spk = [], []
        for x in placed:
            for s, e, t in split_subtitle(x["text"], x["start"], x["end"]):
                scene_subs.append((s, e, t))
                scene_subs_spk.append((s, e, f"{x['name']}: {t}"))
        write_srt(audio_dir / "scenes" / f"{tag}.srt", scene_subs)

        full_pcm += buf
        full_subs += [(s + offset, e + offset, t) for s, e, t in scene_subs]
        full_subs_spk += [(s + offset, e + offset, t) for s, e, t in scene_subs_spk]

        report.append(f"## Cảnh {n} — {sc.get('title', '')}  (bắt đầu {srt_ts(offset)} trong file tổng)")
        report.append("| Panel | Nhân vật | Bắt đầu | Kết thúc | Thời lượng | Câu |")
        report.append("|---|---|---|---|---|---|")
        for x in placed:
            report.append(f"| {x['panel']} | {x['name']} | {x['start']:.2f}s | {x['end']:.2f}s | "
                          f"{x['end'] - x['start']:.2f}s | {x['text']} |")
        report.append("")
        offset += total

    if only_scene is None:
        with tempfile.TemporaryDirectory() as td:
            tmpw = Path(td) / "full.wav"
            write_pcm(tmpw, bytes(full_pcm))
            wav_to_mp3(tmpw, audio_dir / "full_voiceover.mp3")
        write_srt(audio_dir / "full_subtitles.srt", full_subs)
        write_srt(audio_dir / "full_subtitles_speaker.srt", full_subs_spk)

    report.insert(3, f"Engine đã dùng: {', '.join(sorted(engines_used)) or '—'}")
    report.insert(4, "")
    if warnings:
        report += ["## ⚠️ Cảnh báo", ""] + [f"- {w}" for w in warnings]
    else:
        report += ["## ✅ Không có cảnh báo — mọi câu nằm trong thời lượng panel/cảnh."]
    report_name = "timing_report.md" if only_scene is None else f"timing_report_canh_{only_scene:02d}.md"
    (audio_dir / report_name).write_text("\n".join(report), encoding="utf-8")

    log(f"Hoàn tất. Tổng thời lượng: {offset:.2f}s. Thư mục: {audio_dir}")
    for w in warnings:
        log("CẢNH BÁO: " + w)


def main() -> None:
    ap = argparse.ArgumentParser(description="Tạo MP3 + SRT lời thoại từ script.json")
    ap.add_argument("--project", help="Thư mục dự án (chứa script.json)")
    ap.add_argument("--scene", type=int, default=None, help="Chỉ tạo 1 cảnh")
    ap.add_argument("--engine", choices=["vieneu", "edge"], default=None, help="Ép dùng 1 engine cho mọi nhân vật")
    ap.add_argument("--list-voices", action="store_true", help="Liệt kê giọng VieNeu-TTS")
    ap.add_argument("--preview", metavar="VOICE", help="Nghe thử 1 giọng (VieNeu preset hoặc vi-VN-...Neural)")
    ap.add_argument("--text", default="Xin chào, đây là giọng đọc thử cho video của bạn.")
    ap.add_argument("--out", default="voice_preview.mp3")
    args = ap.parse_args()

    if not FFMPEG:
        raise SystemExit("Cần cài ffmpeg (winget install Gyan.FFmpeg) và có trong PATH.")

    if args.list_voices:
        synth = Synthesizer(Path(tempfile.gettempdir()) / "sb_tts_cache")
        for desc, vid in synth.list_vieneu_voices():
            print(f"{vid:20s} | {desc}")
        print(f"{EDGE_MALE:20s} | edge-tts Nam")
        print(f"{EDGE_FEMALE:20s} | edge-tts Nữ")
        return

    if args.preview:
        synth = Synthesizer(Path(tempfile.gettempdir()) / "sb_tts_cache")
        eng = "edge" if args.preview.startswith("vi-VN-") else "vieneu"
        wav, used = synth.synth(args.text, {"engine": eng, "voice": args.preview})
        wav_to_mp3(wav, Path(args.out))
        log(f"Đã tạo {args.out} ({used})")
        return

    if not args.project:
        ap.error("--project là bắt buộc")
    build(Path(args.project).resolve(), args.scene, args.engine)


if __name__ == "__main__":
    main()
