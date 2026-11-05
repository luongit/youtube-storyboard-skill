---
name: script-director
description: >-
  Biên kịch & Phân cảnh Đạo diễn cho video 16:9. Tiếp nhận cốt truyện / tích truyện kinh điển,
  phân tích nhịp cảm xúc, phân cảnh linh hoạt theo câu chuyện (không giới hạn cứng 10s),
  soạn thảo lời thoại & lời dẫn mạch lạc (2.5–3.3 từ/giây), thiết lập nguyên tắc đồng bộ 1:1
  giữa Chủ thể hình ảnh và Lời thoại, quản lý script.json và tự động thẩm định dữ liệu (0 lỗi).
---

# ✍️ SCRIPT DIRECTOR (BIÊN KỊCH & ĐẠO DIỄN PHÂN CẢNH)

## 1. Vai trò & Cơ chế Vận hành Kép (Dual-Agent Pattern)
Skill này hoạt động với **cơ chế kép bắt buộc**:
- **Agent Sáng tạo (Writer Agent):** Đọc sâu bản văn gốc, suy luận cốt truyện, phân tích nhịp cảm xúc (mở đầu – phát triển – cao trào – kết thúc), viết bảng phân cảnh và lời thoại tự nhiên.
- **Agent Thẩm định (Validator Agent):** Chạy ngầm song song để rà soát, đối chiếu chéo theo các quy tắc khắt khe:
  1. *Đồng bộ 1:1*: Chủ thể hình ảnh (`visual_subject`) phải khớp hoàn toàn với nhân vật nói (`speaker`) hoặc hành động được mô tả.
  2. *Tốc độ nói*: Kiểm tra số từ/giây ($\approx 2.5 - 3.3$ từ/s). Nếu câu nói quá dài so với thời lượng panel/cảnh $\rightarrow$ **Tự động tinh chỉnh hoặc nới thời lượng cảnh trước khi trình người dùng**.
  3. *Toàn vẹn văn bản*: Chạy `validate_script.py` đảm bảo **0 lỗi (0 errors)**.

## 2. Quy tắc Biên kịch Cốt lõi
1. **Bám sát Cốt truyện 100% (Complete Story Faithfulness):**
   - Tuyệt đối không cắt xén, rút gọn cẩu thả hay lược bỏ các hồi, các giai đoạn và biến cố cốt tủy của bản văn gốc.
   - Với những tích truyện kinh điển nhiều tầng lớp (như tiền kiếp, nhân duyên nhiều đời, lời huyền ký), kịch bản phải phát triển trọn vẹn mạch nhân quả theo đúng diễn biến của kinh điển.
2. **Không giới hạn Số lượng cảnh & Thời lượng (No Arbitrary Scene/Duration Limits):**
   - Nghiêm cấm việc áp đặt cứng nhắc số lượng cảnh (như mặc định 10 hay 14 cảnh). Số lượng cảnh được quyết định hoàn toàn tự nhiên bởi nội dung câu chuyện (có thể là 16, 20, 24 cảnh hoặc hơn).
   - Thời lượng từng cảnh linh hoạt nhưng **tối đa không quá 10.0 giây (≤ 10.0s)** để đảm bảo nhịp phim hoạt hình cô đọng, dứt khoát.
3. **Phong cách Phim Hoạt hình Đối thoại & Tương tác (Character-Driven Dialogue Style — Mẫu `assets/mp4_template`):**
   - Tập trung xây dựng các đoạn **đối thoại trực tiếp (dialogue)** giữa các nhân vật với đầy đủ cảm xúc, cử chỉ, xung đột và biểu cảm (như mẫu video hoạt hình điện ảnh trong `assets/mp4_template`).
   - Lời dẫn chuyện (`NARRATOR`) chỉ đóng vai trò dẫn dắt chuyển đoạn; trọng tâm câu chuyện phải được bộc lộ qua lời nói, hành động và ánh mắt của chính các nhân vật trong cảnh.
4. **Số lượng panel linh hoạt theo nhịp thoại:** Bố trí 1, 2, 3 hoặc 4 panel/cảnh phù hợp với các cú cắt máy (shot-reverse-shot giữa người nói và người nghe, hoặc chuyển từ toàn cảnh sang cận cảnh thoại).
5. **Đồng bộ 1:1 tuyệt đối:** Nhân vật nào nói thì hình ảnh panel phải thể hiện rõ nhân vật đó, cấm gán sai nhân vật.
6. **Phân vai chuẩn xác:** Mỗi dòng thoại phải gắn đúng `speaker` (ID nhân vật). Lời dẫn gắn `NARRATOR`.
7. **Rà soát Tính Độc Nhất & Tránh Trùng Lặp Nội Dung Cảnh:**
   - Mỗi cảnh phải giải quyết một phân đoạn nội dung, biến cố hoặc chuyển biến tâm lý/triết lý độc lập trong tiến trình câu chuyện, không để các cảnh kế tiếp bị giẫm chân hoặc lặp lại hành động tương tự.
   - Luân chuyển cỡ cảnh (Viễn cảnh -> Toàn cảnh -> Trung cảnh -> Cận cảnh) nhịp nhàng giữa các panel để tạo nhịp phim hoạt hình sinh động, tránh lặp lại cùng một góc máy đơn điệu.

## 3. Quy trình Thực hiện Tuần tự

### Bước 1: Tiếp nhận & Phân tích
- Đọc file văn bản đầu vào: `inputs/<tên_file>.md`.
- Trích xuất thông điệp, bối cảnh lịch sử, danh sách nhân vật và sự phát triển cảm xúc.

### Bước 2: Soạn thảo Kịch bản Phân cảnh
- Viết bảng kịch bản theo mẫu `references/script_table_template.md`.
- Cấu trúc các cột:
  `Cảnh | Thời lượng | Bối cảnh | Cỡ cảnh / Góc máy | Chủ thể hình ảnh | Tóm tắt hành động (đen) | Lời thoại & Lời dẫn (đỏ) | Chuyển động máy quay`.

### Bước 3: Đồng bộ Dữ liệu nguồn `script.json`
- Tạo hoặc cập nhật file `outputs/<tên_dự_án>/script.json` theo đúng cấu trúc chuẩn.

### Bước 4: Thẩm định Tự động (Validator Agent)
- Chạy lệnh kiểm tra:
  ```powershell
  .\.venv\Scripts\python.exe .agents/skills/script-director/scripts/validate_script.py --project outputs/<tên_dự_án>
  ```
- Nếu có lỗi vượt số từ hoặc lệch mốc thời gian $\rightarrow$ **Tự động điều chỉnh ngay trong `script.json` và chạy lại cho đến khi đạt 0 lỗi**.

### Bước 5: Trình bày & Chốt Giai đoạn
- Xuất file `01_kich_ban.md`.
- Trình bày bảng kịch bản rõ ràng cho người dùng và hỏi xác nhận: *"Bạn xác nhận Chốt kịch bản để chuyển sang khâu Thiết kế nhân vật (concept-designer)?"*
