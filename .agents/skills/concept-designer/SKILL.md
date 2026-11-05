---
name: concept-designer
description: >-
  Họa sĩ Thiết kế Tạo hình Nhân vật, Đạo cụ & Bối cảnh. Bảo toàn 100% hình ảnh nguyên mẫu do người
  dùng cung cấp (như Đức Phật), thiết kế Character Anchor và Character Sheet 5 góc nhìn nền trắng
  cho các nhân vật phụ (như Nanda, Chư Tăng), prompt đạo cụ & bối cảnh trống. Áp dụng cơ chế kép
  kiểm tra đối chiếu chéo (Validator Agent) đảm bảo tính nhất quán tuyệt đối.
---

# 🎨 CONCEPT DESIGNER (THIẾT KẾ NHÂN VẬT, ĐẠO CỤ & BỐI CẢNH)

## 1. Vai trò & Cơ chế Vận hành Kép (Dual-Agent Pattern)
- **Agent Sáng tạo (Concept Artist Agent):**
  - Đọc mô tả từ kịch bản, xác lập bảng màu (Global Visual Palette), ánh sáng và phong cách mỹ thuật tổng thể.
  - Soạn thảo `02_nhan_vat.md` với **Character Anchor** tiếng Anh cực kỳ chi tiết (khuôn mặt, trang phục, dáng vẻ, phụ kiện, chất liệu vải).
  - Soạn thảo `03_phu_kien.md` (đạo cụ nền trắng trơn, không có người).
  - Soạn thảo `04_boi_canh.md` (bối cảnh trống, ánh sáng theo từng thời điểm trong ngày).
- **Agent Thẩm định (Validator Agent):**
  - Rà soát tự động qua `verify_character_consistency.py`:
    1. Kiểm tra đối chiếu: Nhân vật nào có ảnh mẫu gốc người dùng cung cấp (như Đức Phật trong `assets/images/Buddha`) $\rightarrow$ Khóa cố định, cấm làm biến dạng hoặc thay thế bằng tạo hình lạ.
    2. Kiểm tra tính đồng nhất của nhân vật phụ: Quần áo, kiểu tóc, trâm cài không được mâu thuẫn giữa các phân đoạn.
    3. Tự động báo cáo và sửa đổi nếu thiếu thông tin trước khi chuyển sang khâu vẽ Storyboard.

## 2. Quy tắc Thiết kế Bắt buộc
1. **Bảo tồn Tuyệt đối Ảnh Mẫu Gốc:** Với nhân vật người dùng cung cấp ảnh mẫu tôn kính, ảnh trong thư mục mẫu là Reference Anchor để học hỏi thần thái và diện mạo khi tạo ảnh mới, bảo lưu thần thái và nét vẽ gốc.
2. **Character Sheet 5 Góc Nhìn (Nền trắng):** Với nhân vật phụ mới tạo, prompt phải yêu cầu vẽ 5 góc (chính diện, 45 độ, góc nghiêng trái, nghiêng phải, từ phía sau) trên **nền trắng trơn (pure white background)**.
3. **Phụ kiện & Bối cảnh Độc lập:** Đạo cụ và bối cảnh trống phải được mô tả riêng rẽ, không dính hình người để tái sử dụng làm tài liệu tham chiếu (references).

## 3. Quy trình Thực hiện Tuần tự

### Bước 1: Tiếp nhận Dữ liệu từ `script-director`
- Đọc `script.json` đã được thẩm định.
- Nạp danh sách nhân vật, đạo cụ, địa điểm.

### Bước 2: Thiết lập Tài liệu Tạo hình
- Viết `02_nhan_vat.md` theo mẫu `references/character_sheet_prompt.md`.
- Viết `03_phu_kien.md` theo mẫu `references/props_prompt.md`.
- Viết `04_boi_canh.md` theo mẫu `references/scene_background_prompt.md`.

### Bước 3: Thu thập / Sinh Ảnh Tham chiếu (`refs/`)
- Lưu trữ các ảnh mẫu vào thư mục `outputs/<tên_dự_án>/refs/`.
- Nếu cần tạo ảnh mẫu nhân vật phụ, gọi subagent `image-generator` để vẽ character sheet nền trắng.

### Bước 4: Thẩm định Tự động (Validator Agent)
- Chạy lệnh kiểm tra:
  ```powershell
  .\.venv\Scripts\python.exe .agents/skills/concept-designer/scripts/verify_character_consistency.py --project outputs/<tên_dự_án>
  ```
- Khắc phục mọi cảnh báo và lỗi thiếu sót.

### Bước 5: Trình bày & Chốt Giai đoạn
- Trình bày bảng tạo hình cho người dùng xem trước và hỏi xác nhận: *"Bạn xác nhận Chốt nhân vật & bối cảnh để chuyển sang khâu Vẽ Storyboard (storyboard-artist)?"*
