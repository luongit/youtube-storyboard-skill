# Character Sheet — 5 góc nhìn, nền trắng

## 1. Mô tả nhân vật (tiếng Việt — để người dùng duyệt)
| Mục | Nội dung |
|---|---|
| Tên / ID | ... / `CHAR_ID` |
| Vai trò | ... |
| Tuổi, giới tính, dáng người | ... (chiều cao tương đối, tỉ lệ đầu/thân theo phong cách) |
| Khuôn mặt | hình mặt, mắt, lông mày, mũi, miệng, nét đặc trưng |
| Tóc | kiểu, màu, độ dài |
| Trang phục | lớp ngoài, lớp trong, màu chính xác, họa tiết, giày dép |
| Phụ kiện gắn liền | (vd. tràng hạt cổ tay phải) — luôn xuất hiện |
| Tính cách → ngôn ngữ cơ thể | ... |
| Giọng đọc | engine + preset (vd. VieNeu "Thiện Minh") |

## 2. Character Anchor (tiếng Anh, 25–45 từ, CỐ ĐỊNH)
Một câu mô tả ngắn, cụ thể, có màu sắc chính xác và vị trí phụ kiện (trái/phải). Dán **nguyên văn** vào mọi prompt
panel / video có nhân vật này. Không dùng từ chung chung ("beautiful", "nice").

> Ví dụ: `AN: a 10-year-old Vietnamese boy, round face, big dark brown eyes, short black bowl-cut hair, faded indigo áo bà ba shirt with wooden buttons, rolled-up black trousers, barefoot, small red string bracelet on left wrist`

## 3. Prompt Character Sheet (copy dùng ở Nano Banana / Midjourney / GPT Image / Flux)
```
Professional character turnaround reference sheet, [ART STYLE].
Character: [CHARACTER ANCHOR].
Five full-body views of the SAME character arranged left to right in one horizontal row, evenly spaced, same scale, same height alignment:
(1) front view facing camera, (2) three-quarter view turned 45 degrees, (3) left side profile, (4) right side profile, (5) back view.
Neutral standing A-pose, relaxed arms, neutral expression, identical outfit, colors, proportions and accessories in every view.
Pure plain white background (#FFFFFF), flat even studio lighting, soft contact shadow only.
No background objects, no scenery, no props other than the character's own accessories, no text, no labels, no watermark.
Generous headroom above head, entire head, hair bun, crown, and hairpins completely visible within frame without cropping.
Clean line art, high detail, model sheet for animation, 16:9.
```
Negative (nếu công cụ hỗ trợ): `cropped head, cut off head, missing hair bun, chopped crown, out of frame head, different outfits, inconsistent face, extra characters, background, scenery, text, labels, cropped feet, extra limbs`

## 4. (Tùy chọn) Bảng biểu cảm khuôn mặt
```
Facial expression sheet of [CHARACTER ANCHOR], [ART STYLE]. 2 rows x 3 head-and-shoulders portraits:
neutral, happy smile, sad, angry, frightened, surprised. Same face, same hairstyle, same outfit collar.
Pure white background, flat studio lighting, no text, 16:9.
```

## 5. Khi tạo ảnh bằng subagent `image-generator`
- Gửi prompt tiếng Anh ở Mục 3, yêu cầu tỷ lệ 16:9, lưu `projects/<slug>/refs/<CHAR_ID>_sheet.png`.
- Sau khi người dùng chốt, ghi đường dẫn vào `characters[].reference_image` trong `script.json`.
- Mọi ảnh panel sau này phải gửi kèm ảnh này làm tham chiếu.
