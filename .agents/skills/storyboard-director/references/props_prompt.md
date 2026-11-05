# Prompt Phụ kiện / Đạo cụ (nền trắng)

Liệt kê **mọi** đồ vật có vai trò trong truyện (vũ khí, đồ dùng, con vật phụ, phương tiện, vật biểu tượng...).
Đồ vật gắn liền nhân vật (vd. tràng hạt) vẫn liệt kê riêng để tạo ảnh cận chi tiết.

## Bảng phụ kiện
| ID | Tên | Xuất hiện ở cảnh | Chủ sở hữu | Mô tả (VI) | Ý nghĩa trong truyện |
|---|---|---|---|---|---|
| `YEN_CUONG` | Yên cương ngựa | 2, 3, 8 | Nhà vua | Yên da nâu viền vàng... | Nguyên nhân xung đột |

## Mẫu prompt (mỗi phụ kiện 1 prompt)
```
Product-style prop reference sheet, [ART STYLE].
Prop: [PROP DESCRIPTION — material, color, size relative to a human hand, wear and texture, decorative details].
Shown from three angles in one horizontal row: front view, three-quarter view, side view. Same object, same scale.
Pure plain white background (#FFFFFF), flat even studio lighting, soft contact shadow.
No people, no hands, no characters, no background objects, no text, no labels, no watermark. 16:9.
```

## Quy tắc
- Mô tả vật liệu + màu + kích thước tương đối để AI video giữ đúng tỉ lệ khi nhân vật cầm.
- Nếu phụ kiện thay đổi trạng thái (vd. yên cương **bị cắn rách**), tạo thêm biến thể: `YEN_CUONG_RACH`.
- Lưu ảnh: `projects/<slug>/refs/prop_<ID>.png`, ghi vào `props[]` trong `script.json`.
