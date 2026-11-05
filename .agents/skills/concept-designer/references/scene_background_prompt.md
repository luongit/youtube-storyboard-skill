# Prompt Bối cảnh trống (chưa có nhân vật)

Mỗi địa điểm 1 prompt gốc + biến thể ánh sáng theo cảm xúc của từng cảnh dùng địa điểm đó.

## Bảng bối cảnh
| ID | Tên | Dùng ở cảnh | Thời điểm / Thời tiết | Cảm xúc | Biến thể ánh sáng |
|---|---|---|---|---|---|
| `NGHIA_DIA` | Nghĩa địa ven rừng | 8, 9 | Đêm trăng, sương mù | Hoảng loạn → hy vọng | Lạnh xanh tím → ánh trăng ấm |

## Mẫu prompt
```
Empty environment background plate for animation, [ART STYLE].
Location: [LOCATION — architecture, nature, key landmarks, materials, cultural details (Vietnamese if relevant)].
Time and weather: [time of day, weather, season].
Mood lighting: [lighting matching the scene emotion, color temperature, key light direction].
Composition: wide establishing shot, eye-level, clear open space in the [foreground/midground center] for characters to be placed later.
Color palette: [GLOBAL PALETTE + scene accent].
Absolutely no people, no characters, no animals, no text, no watermark. Cinematic, highly detailed, 16:9.
```

## Bảng màu theo cảm xúc (gợi ý)
| Cảm xúc | Ánh sáng | Màu |
|---|---|---|
| Bình yên | Nắng sớm mềm, bóng dài | Vàng ấm, xanh lá nhạt |
| Hồi hộp / sợ hãi | Tương phản cao, ngược sáng, sương | Xanh lạnh, tím, đen sâu |
| Giận dữ | Ánh lửa, đỏ gắt, bóng cứng | Đỏ, cam, đen |
| Buồn | Ánh sáng tán, mưa, chiều tà | Xám xanh, khử bão hòa |
| Hy vọng / giác ngộ | Tia sáng xuyên mây, viền sáng | Vàng kim, trắng ấm |

Lưu ảnh: `projects/<slug>/refs/loc_<ID>.png`, ghi vào `locations[]` trong `script.json`.
