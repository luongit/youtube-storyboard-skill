---
name: storyboard-artist
description: >-
  Họa sĩ Storyboard & Xếp Lưới Caption. Vẽ / xử lý panel 16:9 Full HD (1920x1080), áp dụng nguyên tắc
  cốt tử Headroom Safety (không bao giờ cắt mất đầu / búi tóc / vương miện / hào quang), kiểm tra
  đồng bộ 1:1 tuyệt đối giữa Nhân vật – Hình ảnh – Lời thoại (không gán sai nhân vật), tự động xếp lưới
  Adaptive Grid Layout kèm caption đen (hành động) và đỏ (lời thoại).
---

# 📐 STORYBOARD ARTIST (HỌA SĨ STORYBOARD & XẾP LƯỚI CAPTION)

## 1. Vai trò & Cơ chế Vận hành Kép (Dual-Agent Pattern)
- **Agent Sáng tạo (Storyboard Artist Agent):**
  - Đọc `script.json` và tài liệu từ `concept-designer`.
  - Sinh hoặc gán ảnh cho từng panel khớp 100% với hành động và lời thoại.
  - Xử lý ảnh sang chuẩn Full HD 16:9 (**1920x1080**) tràn viền (không dùng dải đen letterbox).
  - Áp dụng kỹ thuật neo crop **Headroom Safety**: `centering=(0.5, 0.10)` sát đỉnh để bảo toàn trọn vẹn phần đầu nhân vật.
  - Ghép lưới thích ứng qua `compose_storyboard.py`.
- **Agent Thẩm định (Validator Agent):**
  - Chạy `verify_panel_alignment.py` để rà soát tự động:
    1. *Kiểm tra lệch vai*: Cấm tuyệt đối việc lời thoại hoặc hành động nói về nhân vật A (như nữ cư sĩ Nanda hay Chư Tăng) mà hình ảnh panel lại là nhân vật B (như Đức Phật).
    2. *Kiểm tra kích thước*: Đảm bảo đúng 1920x1080.
    3. *Tự động chặn và sửa*: Nếu phát hiện lệch chủ thể $\rightarrow$ Tự động thay đổi nguồn ảnh chuẩn xác trước khi xuất ảnh lưới cho người dùng.

## 2. Quy tắc Storyboard Cốt tử
1. **TƯ DUY & TẠO ẢNH MỚI PHÙ HỢP 100% (KHÔNG CẮT GHÉP MÁY MÓC):**
   - Kho ảnh trong `assets/images/` là **ẢNH THAM KHẢO TẠO HÌNH (REFERENCE ANCHORS)** để định vị diện mạo, trang phục, dáng vẻ và phong cách mỹ thuật cổ trang Phật giáo.
   - Tuyệt đối **không được lấy ảnh gốc crop rồi ghép máy móc** vào storyboard!
   - Agent phải **tư duy độc lập để tạo ảnh mới (Generate Images)** thông qua subagent `image-generator` với mô tả hành động, cỡ cảnh, góc máy, ánh sáng và biểu cảm cảm xúc ăn khớp 100% với kịch bản của từng panel.
2. **ĐỒNG BỘ 1:1 TUYỆT ĐỐI GIỮA NHÂN VẬT - HÌNH ẢNH - LỜI THOẠI:**
   - Panel nói về Vua -> Tạo hình vị vua uy nghiêm theo đúng phong thái tham khảo `assets/images/Đức Vua/`.
   - Panel nói về Ngạ quỷ -> Tạo hình bầy ngạ quỷ đói khổ theo mẫu tham khảo `assets/images/Ngạ quỷ đối/`.
   - Panel nói về Tướng quân / Hoàng tử -> Tạo hình chiến binh dũng mãnh theo mẫu `assets/images/Tướng quân/`.
   - Panel về Chư Tăng -> Tạo hình Tỳ kheo thanh tịnh theo mẫu `assets/images/Tỳ kheo/`.
   - Panel về Đức Phật -> Bám sát 100% thần thái từ mẫu `assets/images/Buddha/`.
3. **BẢO VỆ KHOẢNG THỞ TRÊN ĐẦU (HEADROOM SAFE):** Mọi khung hình có nhân vật phải chừa khoảng thở phía trên đầu (`generous headroom`). Không bao giờ được để mép trên cắt cụt đầu, nhục kế, búi tóc hay vương miện.
4. **BỐ CỤC LƯỚI THÍCH ỨNG (ADAPTIVE GRID):**
   - 1 panel: Toàn màn hình.
   - 2 panels: 2x1 (ngang).
   - 3 panels: 3x1 (ngang).
   - 4 panels: 2x2.
   - 5–6 panels: 3x2.
5. **MÀU SẮC CAPTION TIÊU CHUẨN:**
   - Số thứ tự và mốc thời gian: Góc trái trên mỗi ô.
   - **HÀNH ĐỘNG**: Chữ in hoa màu **ĐEN**.
   - **THOẠI - TÊN NHÂN VẬT**: Chữ in hoa màu **ĐỎ**.

## 2.1. Quy tắc Soạn Prompt Storyboard Chi Tiết, Giới Hạn Thời Lượng & Đóng Gói Một Khối Duy Nhất (Prompting Standards)
Mỗi cảnh trong bộ Prompt Storyboard bắt buộc phải tuân thủ nghiêm ngặt các yêu cầu sau:

1. **Giới Hạn Thời Lượng Cảnh (Tối đa 10s/cảnh):**
   - Mỗi cảnh video có thời lượng **tối đa không quá 10.0 giây** (ví dụ: Panel 1 từ 0.0s - 5.0s, Panel 2 từ 5.0s - 10.0s; hoặc phân bổ linh hoạt 4s + 6s nhưng tổng không vượt quá 10s).
   - Đảm bảo nhịp dựng phim nhanh, cô đọng, giàu cảm xúc, phù hợp với định dạng video ngắn và chuyển động hoạt hình điện ảnh.

2. **Rà soát Tính Độc Nhất & Tránh Trùng Lặp Nội Dung Cảnh:**
   - Mỗi cảnh phải có một bước chuyển mạch truyện, hành động hoặc thông điệp giáo lý rõ ràng, không trùng lặp hay giẫm chân lên các cảnh trước và sau nó.
   - Luân chuyển góc máy nhịp nhàng (Viễn cảnh, Toàn cảnh, Trung cảnh, Cận cảnh).

3. **Cấu Trúc Đóng Gói Thành MỘT KHỐI CODE DUY NHẤT (Single Code Block) Cho Mỗi Cảnh:**
   - Toàn bộ nội dung prompt của một cảnh (bao gồm cả tiếng Việt chỉ dẫn bối cảnh, mốc thời gian, góc máy, thoại, dẫn và prompt tiếng Anh) phải nằm trọn vẹn trong **ĐÚNG 1 KHỐI CODE (` ```text `)**.
   - Người dùng chỉ cần bấm nút "Copy" khối code đó, tải ảnh tham chiếu lên công cụ AI và dán thẳng vào để sinh ảnh, không phải chắp vá hay tìm kiếm file trên máy.
   - Mẫu chuẩn bắt buộc của khối prompt:
   ```text
   Tạo ảnh storyboard chi tiết các khung hình cho đoạn video theo mô tả sau
   Tiêu đề: CẢNH [Số]: [TÊN CẢNH] (Thời lượng: [Tối đa 10.0s])
   - Địa điểm: [TÊN ĐỊA ĐIỂM] (Tham chiếu ảnh đính kèm)
   - Tone cảm xúc: [Cảm xúc]
   - Bối cảnh tổng quan: [Mô tả tổng quan bối cảnh]

   CHI TIẾT CÁC PHÂN CẢNH (PANELS):
   Panel 1:
   - Thời gian: `0.0s - 5.0s` (Thời lượng: 5.0s)
   - Cỡ cảnh & Góc máy: [Cỡ cảnh + chuyển động máy]
   - Chủ thể hình ảnh: [Tên chủ thể] (Tham chiếu ảnh đính kèm)
   - Lời dẫn: "[Lời dẫn nếu có hoặc *Không có*]"
   - Lời thoại: "[Lời thoại nếu có hoặc *Không có*]"
   - Mô tả bối cảnh & Hành động: [Mô tả chi tiết hành động và bố cục]

   Panel 2:
   - Thời gian: `5.0s - 10.0s` (Thời lượng: 5.0s)
   - Cỡ cảnh & Góc máy: [Cỡ cảnh + chuyển động máy]
   - Chủ thể hình ảnh: [Tên chủ thể] (Tham chiếu ảnh đính kèm)
   - Lời dẫn: "[Lời dẫn nếu có hoặc *Không có*]"
   - Lời thoại: "[Lời thoại nếu có hoặc *Không có*]"
   - Mô tả bối cảnh & Hành động: [Mô tả chi tiết hành động và bố cục]

   Bối cảnh chung
   [Prompt tiếng Anh chi tiết: Thiết lập bối cảnh, chỉ dẫn tham chiếu ảnh đính kèm: 'Please strictly reference the attached image...', chi tiết Panel 1, Panel 2, Art Style, --ar 16:9, negative parameters]
   ```

## 3. Quy trình Thực hiện Tuần tự

### Bước 1: Tiếp nhận Kịch bản & Dữ liệu Tham chiếu
- Đọc `script.json` từ `script-director` và ảnh trong `refs/` từ `concept-designer`.

### Bước 2: Chuẩn bị & Xử lý Ảnh Panel
- Sinh ảnh bằng subagent `image-generator` hoặc lấy ảnh chuẩn từ thư viện.
- Xử lý crop bằng Pillow với tỷ lệ 16:9 và neo `centering=(0.5, 0.10)`.
- Lưu vào `outputs/<tên_dự_án>/05_storyboard/canh_NN/panel_XX.png`.

### Bước 3: Ghép Lưới Storyboard Tự Động
- Chạy lệnh:
  ```powershell
  .\.venv\Scripts\python.exe .agents/skills/storyboard-artist/scripts/compose_storyboard.py --project outputs/<tên_dự_án> --scene N
  ```
- Kết quả tạo ra `outputs/<tên_dự_án>/05_storyboard/storyboard_canh_NN.png`.

### Bước 4: Thẩm định Tự Động (Validator Agent)
- Chạy lệnh kiểm tra:
  ```powershell
  .\.venv\Scripts\python.exe .agents/skills/storyboard-artist/scripts/verify_panel_alignment.py --project outputs/<tên_dự_án> [--scene N]
  ```
- Nếu phát hiện lỗi lệch nhân vật $\rightarrow$ Tự động gán lại ảnh đúng và xếp lưới lại.

### Bước 5: Xuất File Tổng Hợp Lời Thoại `voice-script.md` (Viết thường 100%)
- Sau khi hoàn thành và thẩm định xong toàn bộ ảnh Storyboard, tự động chạy lệnh:
  ```powershell
  .\.venv\Scripts\python.exe .agents/skills/storyboard-artist/scripts/generate_voice_script.py outputs/<tên_dự_án>
  ```
- Kết quả tạo ra file `outputs/<tên_dự_án>/voice-script.md`.
- **Quy tắc bắt buộc:** Toàn bộ nội dung lời thoại và lời dẫn trong file đều được chuyển thành **chữ thường (lowercase, không in hoa)**, bao gồm 2 phần:
  1. *Kịch bản đọc liền mạch*: Toàn bộ câu từ nối tiếp nhau bằng chữ thường để đọc thu âm trơn tru một mạch.
  2. *Kịch bản phân vai theo từng cảnh*: Từng câu thoại kèm nhân vật đều viết chữ thường.

### Bước 6: Điểm Dừng Duyệt (Core Milestone Checkpoint)
- **ĐÂY LÀ ĐIỂM DỪNG HOÀN THÀNH BỘ STORYBOARD CỐT LÕI**.
- Bàn giao trọn bộ:
  - Thư mục ảnh panel `05_storyboard/canh_NN/panel_XX.png`
  - Các ảnh lưới storyboard `05_storyboard/storyboard_canh_NN.png`
  - File tổng hợp lời thoại chữ thường `voice-script.md`
- Trình bày cho người dùng và hỏi:
  *"Bộ Storyboard tĩnh và file lời thoại `voice-script.md` đã hoàn thành trọn vẹn và đạt chuẩn 100%. Bạn có muốn tiếp tục bước sang khâu Lồng tiếng AI (voice-audio-engineer) và Dựng video (video-animator) không?"*