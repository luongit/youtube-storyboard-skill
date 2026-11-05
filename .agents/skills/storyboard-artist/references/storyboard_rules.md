# Quy tắc Storyboard (Giai đoạn 3)

## 1. Bố cục ảnh lưới linh hoạt (Adaptive Layout)
- 1 cảnh (10 giây) = **1 ảnh storyboard** dạng lưới ngang. Số lượng panel linh hoạt từ **1 đến 6 panel** (tối đa 8) tùy thuộc vào nhịp điệu hành động và độ dài câu thoại của nhân vật:
  - **1 panel** → 1 khung hình lớn 16:9 (Long take / Master shot / Lia chậm 10s).
  - **2 panels** → Lưới ngang 2×1 (Thiết lập + Cận cảnh thoại, hoặc Đối kháng 2 nhân vật).
  - **3 panels** → Lưới ngang 3×1 (Mở nhịp + Thoại chính + Phản ứng).
  - **4 panels** → Lưới 2×2 chuẩn.
  - **5–6 panels** → Lưới 3×2 (Giao tranh dồn dập, chuyển cảnh nhanh, đối đáp nhiều câu ngắn).
  - **7–8 panels** → Lưới 3×3 (Montage hành động cực nhanh).
- **Số thứ tự** (1, 2, 3...) + mốc thời gian ở góc trên trái mỗi ô.
- **Dải băng trắng dưới mỗi ô**, tách rõ ràng:
  - Màu **đen**: `HÀNH ĐỘNG: <shot> – <mô tả hành động, tương tác và biểu cảm>`
  - Màu **đỏ**: `THOẠI – <TÊN NHÂN VẬT>: "<câu thoại>"` hoặc `THOẠI: Không thoại`
  - Lời dẫn (nếu có): màu xám đậm `LỜI DẪN: "..."` — để AI video **không** tạo khẩu hình cho lời dẫn.
- Tiêu đề trên cùng: `CẢNH N — <TÊN CẢNH> · Thời lượng 10 giây`.

> **Vì sao ghép bằng script?** AI tạo ảnh thường viết sai tiếng Việt có dấu. Ta tạo ảnh từng panel **không chữ**,
> rồi script vẽ số + caption bằng font hệ thống → chữ chuẩn, màu chuẩn, đồng thời có sẵn ảnh rời từng panel
> để làm keyframe cho AI video (image-to-video / animatics).

## 2. Đồng bộ chặt chẽ: Hành động – Biểu cảm – Lời thoại – Thời lượng (Strict Sync)
Mỗi panel bắt buộc phải có thời lượng tương ứng với nội dung diễn biến:
1. **Khớp nhân vật & khẩu hình**:
   - Nếu panel có thoại của nhân vật A: khung hình **bắt buộc** phải là Cận cảnh (Close-up), Trung cận (Medium close-up) hoặc Qua vai (Over-the-shoulder) tập trung vào nhân vật A, với biểu cảm và khẩu hình mở phù hợp nội dung câu thoại.
   - Nếu panel là đại cảnh hoặc chỉ có hành động (chém kiếm, bay lượn, lướt mây, thi triển pháp bảo): ghi rõ `THOẠI: Không thoại` để AI video không tự chế lời hoặc khẩu hình lung tung.
2. **Khớp thời lượng (Timing)**:
   - Tốc độ nói tiếng Việt chuẩn là ~3 đến 3.3 từ/giây.
   - Panel dài 2s: Thoại tối đa 6–7 từ.
   - Panel dài 4s: Thoại từ 10–13 từ.
   - Panel dài 6s–8s: Thoại dài sâu lắng từ 18–25 từ.

## 3. Chuyển động máy quay & Nhịp độ (Dynamic Camera Motion & Velocity)
Mỗi panel trong kịch bản phải chỉ định rõ `camera_motion` để tạo nhịp điệu phong phú, tránh nhàm chán:
| Camera Motion | Tên tiếng Việt | Hiệu ứng thị giác & Thời điểm sử dụng |
|---|---|---|
| `slow_pan_right` / `slow_pan_left` | Lia máy chậm | Quét ngang qua đại cảnh hùng vĩ, quảng trường tông môn, biển mây, hoặc hàng dài đệ tử. |
| `slow_push_in` | Zoom chậm vào tâm | Đẩy nhẹ vào gương mặt nhân vật khi đang nói lời thâm trầm, suy tư hoặc bộc lộ cảm xúc sâu sắc. |
| `fast_push_in` / `dramatic_zoom` | Zoom nhanh dồn dập | Phóng nhanh vào ánh mắt sắc lạnh, trúng đòn bất ngờ, hoặc khoảnh khắc rút kiếm/thi triển pháp bảo. |
| `slow_pull_out` | Thu máy lùi dần | Kéo từ cận cảnh ra toàn cảnh, hé lộ bối cảnh to lớn xung quanh hoặc cảm giác cô độc/thanh thản. |
| `static` | Máy quay tĩnh | Giữ khung hình tôn nghiêm, tĩnh lặng, trang trọng (thích hợp cho các đại sư ngồi thiền, ngai vàng). |

Quy tắc: tuân thủ **trục 180°** trong đối thoại; xen kẽ cỡ cảnh (rộng → trung → cận); hướng di chuyển nhất quán
giữa các panel; panel cuối của cảnh nên tạo cầu nối sang cảnh sau.

## 4. Quy tắc Khung hình Full HD & Bảo vệ Đầu Nhân Vật (Headroom Safety Rule)
1. **Khung hình Full HD chuẩn 16:9 (Không viền đen)**:
   - Tất cả hình ảnh và video animatic mặc định render **Full 1920x1080 (16:9 tràn khung hình)**, không thêm dải đen letterbox để tận dụng 100% diện tích màn hình hiển thị trên YouTube và TV.
2. **CỰC KỲ QUAN TRỌNG — KHÔNG BAO GIỜ CẮT MẤT ĐẦU NHÂN VẬT**:
   - **Bố cục khung hình (Headroom)**: Mọi shot hình có nhân vật (từ Viễn cảnh, Toàn cảnh đến Cận cảnh) **bắt buộc** phải chừa một khoảng trống an toàn bên trên đầu (`generous headroom above head`).
   - **Bảo toàn chi tiết trang sức/tóc**: Toàn bộ đỉnh đầu, búi tóc, trâm cài tóc, vương miện hoặc dải lụa trên đầu nhân vật phải nằm trọn vẹn bên trong khung hình, tuyệt đối không bị đường viền trên cắt đứt.
   - **Góc cận cảnh chuẩn**: Với cảnh cận cảnh, dùng `Head-and-shoulders medium close-up with ample headroom`, KHÔNG dùng cận cảnh quá sát (extreme tight close-up) làm cụt trán hoặc mất tóc.
   - **An toàn khi Zoom Pan**: Script dựng video neo trục Y ở vị trí cao (`y='max(0, (ih-ih/zoom)*0.15)'`) để chuyển động máy quay không bao giờ lấn vào vùng đỉnh đầu.

## 5. Prompt ảnh từng panel (tiếng Anh)
```
[ART STYLE]. Storyboard keyframe, 16:9 Full HD, cinematic composition.
Generous headroom, complete head and hair headdress fully visible inside frame, do not crop top of head.
Shot: [shot type + camera angle + lens].
Characters: [CHARACTER ANCHOR(S) — nguyên văn], [pose, action, facial expression, gaze direction].
Props: [prop description if any].
Setting: [LOCATION prompt rút gọn], [time of day].
Lighting & color: [mood lighting for this scene emotion].
Keep character design identical to the reference sheet. No text, no captions, no speech bubbles, no panel borders, no watermark.
```
Negative prompt (bắt buộc): `cropped head, cut off head, cut off hair, out of frame hairpins, missing crown, tight top crop`
Khi gọi `image-generator`: đính kèm đường dẫn ảnh tham chiếu nhân vật (`refs/<CHAR_ID>_sheet.png`), bối cảnh
(`refs/loc_<ID>.png`) và lưu đúng `05_storyboard/canh_NN/panel_XX.png`. Cập nhật `image` trong `script.json`.

## 6. Prompt lưới 1 ảnh (cho công cụ ngoài)
Người dùng có thể muốn tạo cả lưới trong 1 lần (Nano Banana, GPT Image...):
```
A single storyboard sheet, [ART STYLE], 16:9 Full HD, white page background, [ROWS]x[COLS] grid of [N] equal panels with thin black borders.
Each panel has its number in the top-left corner and a white caption strip beneath it.
Ample headroom in all character panels, full heads and hair ornaments fully visible.
Panel 1: [shot], [action with character anchors]. Caption black: "HÀNH ĐỘNG: ...". Caption red: "THOẠI: Không thoại".
Panel 2: ...
Consistent character design across all panels matching the reference sheet; lighting and color mood: [mood].
```
⚠️ Ghi chú cho người dùng: chữ tiếng Việt do AI tự vẽ có thể sai dấu — nên dùng ảnh do script ghép.

## 7. File `05_storyboard/canh_NN.md`
1. Bảng panel (Panel | Thời gian | Shot | Hành động | Thoại)
2. Prompt ảnh từng panel
3. Prompt lưới 1 ảnh
4. Prompt video từng panel (xem `video_prompt_guide.md`)
5. Ghi chú âm thanh: SFX, nhạc nền, chỗ cần im lặng
6. Ảnh: `![Cảnh N](canh_NN/../storyboard_canh_NN.png)`
