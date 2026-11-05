---
name: voice-audio-engineer
description: >-
  Kỹ sư Âm thanh & Lồng tiếng AI (Tùy chọn). Tạo giọng đọc tiếng Việt bằng VieNeu-TTS với công nghệ
  Zero-shot Voice Cloning trích xuất từ file mẫu MP3/WAV của người dùng, căn chỉnh mốc thời gian
  từng câu thoại theo panel, xuất file MP3 cảnh và phụ đề chuẩn .srt cho CapCut / Premiere.
---

# 🎙️ VOICE & AUDIO ENGINEER (KỸ SƯ ÂM THANH & LỒNG TIẾNG AI)

## 1. Vai trò & Cơ chế Vận hành Kép (Dual-Agent Pattern)
- **Agent Sáng tạo (Audio Engineer Agent):**
  - Đọc phân vai thoại từ `script.json`.
  - Quản lý engine **VieNeu-TTS** (hỗ trợ 25 giọng preset tiếng Việt tự nhiên và Zero-shot Voice Cloning từ file mẫu).
  - Tách ghép mốc thời gian câu thoại, tạo khoảng nghỉ tự nhiên (`LINE_LEAD_IN`, `LINE_GAP`).
  - Xuất các file âm thanh rời, âm thanh ghép cảnh (`canh_NN.mp3`), âm thanh tổng hợp (`full_voiceover.mp3`) và file phụ đề `.srt`.
- **Agent Thẩm định (Validator Agent):**
  - Chạy `verify_audio_sync.py` đối chiếu tự động:
    1. Kiểm tra thời lượng âm thanh thực tế so với thời lượng dự kiến trong `script.json`.
    2. Nếu câu nói bị dài hơn thời lượng panel $\rightarrow$ Tự động cảnh báo và đề xuất đồng bộ lại độ dài video.
    3. Đảm bảo 100% các file phụ đề `.srt` khớp mốc thời gian từng mili-giây.

## 2. Các Chế độ Giọng đọc Hỗ trợ
1. **Zero-shot Voice Cloning (Theo mẫu MP3 của bạn):**
   - Đặt file mẫu trong `assets/mp3-template/`.
   - Cấu hình trong `script.json`:
     ```json
     "voice": {
       "engine": "vieneu",
       "voice": "Thiền Tâm Đức",
       "ref_audio": "assets/mp3-template/03-dong-buddha.mp3",
       "speed": 0.95
     }
     ```
2. **25 Giọng Preset Chuẩn Tiếng Việt:**
   - Nam Bắc: `Thiện Minh` (kể chuyện), `Hải Đăng` (tự nhiên), `Adam bựa` (hài hước).
   - Nữ Bắc: `Trúc Ly` (dịu dàng), `Mai Anh` (tin tức).
   - Thiền/Tôn giáo: `Thiền Tâm Đức` (trầm hùng, sâu lắng).

## 3. Quy trình Thực hiện Tuần tự

### Bước 1: Tiếp nhận Thoại & Cấu hình Giọng
- Đọc `script.json` hoặc file `voice-script.md` (bản tổng hợp lời thoại viết thường toàn bộ đã được tạo từ khâu storyboard).
- Khớp file mẫu giọng trong `assets/mp3-template/` với từng nhân vật.

### Bước 2: Sinh Âm thanh & Phụ đề Tự động
- Chạy lệnh:
  ```powershell
  .\.venv\Scripts\python.exe .agents/skills/voice-audio-engineer/scripts/dialogue_tts_srt.py --project outputs/<tên_dự_án> [--scene N]
  ```
- Kết quả sinh ra:
  - `audio/scenes/canh_NN.mp3` & `canh_NN.srt`
  - `audio/full_voiceover.mp3` & `full_subtitles.srt`
  - `audio/timing_report.md`

### Bước 3: Thẩm định Tự động (Validator Agent)
- Chạy lệnh kiểm tra:
  ```powershell
  .\.venv\Scripts\python.exe .agents/skills/voice-audio-engineer/scripts/verify_audio_sync.py --project outputs/<tên_dự_án>
  ```
- Đảm bảo toàn bộ file audio và srt đạt chuẩn trước khi chuyển sang khâu dựng video.
