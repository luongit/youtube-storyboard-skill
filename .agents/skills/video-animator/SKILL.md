---
name: video-animator
description: >-
  Dựng phim Animatic & Ghép Master Video (Tùy chọn). Sử dụng FFmpeg tạo chuyển động máy quay điện ảnh
  Ken Burns đa tốc độ (push-in, pan, pull, static), áp dụng neo trục Y an toàn bảo toàn headroom
  (không mất đầu nhân vật), ghép đồng bộ hình ảnh với âm thanh thoại từng cảnh, sau đó ghép nối
  toàn bộ thành video master 1080p hoàn chỉnh, tràn viền không viền đen.
---

# 🎬 VIDEO ANIMATOR (DỰNG PHIM ANIMATIC & MASTER VIDEO)

## 1. Vai trò & Cơ chế Vận hành Kép (Dual-Agent Pattern)
- **Agent Sáng tạo (Video Animator Agent):**
  - Đọc `script.json`, ảnh panel từ `storyboard-artist` và âm thanh từ `voice-audio-engineer`.
  - Thiết lập bộ lọc FFmpeg zoompan mô phỏng chuyển động máy quay đa tốc độ (`slow_pan_right`, `slow_push_in`, `fast_push_in`, `slow_pull_out`, `static`).
  - **Khóa an toàn vùng đầu (Headroom Safe Y-Anchor):** Neo trục Y `y='max(0,(ih-ih/zoom)*0.15)'` để chuyển động máy quay zoom/pan tuyệt đối không lấn vào vùng đỉnh đầu, búi tóc hay vương miện nhân vật.
  - Ghép đồng bộ hình ảnh với file âm thanh thoại `canh_NN.mp3` của cảnh.
  - Ghép nối tất cả các cảnh thành video master hoàn chỉnh `full_video.mp4`.
- **Agent Thẩm định (Validator Agent):**
  - Chạy `verify_video_output.py` dùng ffprobe đối chiếu:
    1. Kiểm tra độ phân giải chuẩn **1920x1080** Full HD (16:9), 30fps H.264 / AAC 48kHz.
    2. Đảm bảo video tràn viền đầy đủ, không có viền đen letterbox.
    3. Kiểm tra tính liên tục và khớp thời lượng giữa âm thanh và hình ảnh.

## 2. Quy trình Thực hiện Tuần tự

### Bước 1: Tiếp nhận Dữ liệu từ các khâu trước
- Ảnh panel trong `outputs/<tên_dự_án>/05_storyboard/canh_NN/panel_XX.png`.
- File âm thanh cảnh trong `outputs/<tên_dự_án>/audio/scenes/canh_NN.mp3`.
- Dữ liệu chuyển động máy quay trong `script.json`.

### Bước 2: Render Video Từng Cảnh
- Chạy lệnh:
  ```powershell
  .\.venv\Scripts\python.exe .agents/skills/video-animator/scripts/render_scene_video.py --project outputs/<tên_dự_án> --scene N
  ```
- Kết quả tạo ra `outputs/<tên_dự_án>/videos/canh_NN.mp4`.

### Bước 3: Ghép Nối Master Video
- Chạy lệnh:
  ```powershell
  .\.venv\Scripts\python.exe .agents/skills/video-animator/scripts/stitch_full_video.py --project outputs/<tên_dự_án>
  ```
- Kết quả tạo ra `outputs/<tên_dự_án>/videos/full_video.mp4`.

### Bước 4: Thẩm định Tự Động (Validator Agent)
- Chạy lệnh kiểm tra:
  ```powershell
  .\.venv\Scripts\python.exe .agents/skills/video-animator/scripts/verify_video_output.py --project outputs/<tên_dự_án>
  ```
- Đảm bảo 100% video cảnh và master video đạt chuẩn xuất bản (0 lỗi).

### Bước 5: Bàn giao Sản phẩm Hoàn chỉnh
- Cung cấp đường dẫn file `full_video.mp4` và bảng tổng hợp thông số kỹ thuật cho người dùng.
