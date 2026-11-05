# Schema `script.json` (nguồn dữ liệu duy nhất của dự án)

```json
{
  "project": "Bồ-tát và đàn chó",
  "slug": "bo-tat-va-dan-cho",
  "aspect_ratio": "16:9",
  "scene_duration_sec": 10,
  "style": {
    "art_style": "2D Vietnamese folk-tale animation, soft cel shading",
    "palette": "warm earth tones, saffron, moss green, dusk purple",
    "lighting": "soft cinematic lighting, adjusted per scene mood",
    "camera": "35mm cinematic framing, shallow depth of field"
  },
  "characters": [
    {
      "id": "BO_TAT",
      "name": "Bồ-tát",
      "role": "Nhân vật chính",
      "voice": { "engine": "vieneu", "voice": "Thiện Minh", "speed": 1.0 },
      "description_vi": "Nam, khoảng 40 tuổi, gương mặt hiền từ...",
      "anchor_en": "a serene Buddhist bodhisattva man around 40, shaved head, calm almond eyes, saffron robe draped over left shoulder, wooden prayer beads on right wrist, barefoot",
      "reference_image": "refs/BO_TAT_sheet.png"
    },
    {
      "id": "NARRATOR",
      "name": "Người dẫn chuyện",
      "role": "Lời dẫn",
      "voice": { "engine": "vieneu", "voice": "Thanh Bình", "speed": 1.0 }
    }
  ],
  "props": [
    { "id": "YEN_CUONG", "name": "Yên cương ngựa", "prompt_en": "...", "reference_image": "refs/prop_YEN_CUONG.png" }
  ],
  "locations": [
    { "id": "NGHIA_DIA", "name": "Nghĩa địa ven rừng", "prompt_en": "...", "reference_image": "refs/loc_NGHIA_DIA.png" }
  ],
  "scenes": [
    {
      "scene": 8,
      "title": "Đàn chó chạy đến cầu cứu Bồ-tát",
      "location": "NGHIA_DIA",
      "mood": "hoảng loạn → hy vọng",
      "visual": "Đàn chó chạy vào nghĩa địa, tụ quanh Bồ-tát...",
      "audio": "Tiếng chó sủa xa, gió rít, nhạc nền căng thẳng chuyển sang trầm ấm",
      "panels": [
        {
          "panel": 1, "start": 0.0, "end": 2.0,
          "shot": "Toàn cảnh",
          "camera_motion": "slow_pan_right",
          "action_vi": "Đàn chó hoảng loạn chạy vào nghĩa địa.",
          "lines": [ { "speaker": "NARRATOR", "text": "Giữa đêm, đàn chó hoảng loạn tìm đến nghĩa địa." } ],
          "image_prompt_en": "...",
          "video_prompt_en": "...",
          "image": "05_storyboard/canh_08/panel_01.png"
        },
        {
          "panel": 2, "start": 2.0, "end": 4.0,
          "shot": "Trung cảnh",
          "camera_motion": "slow_push_in",
          "action_vi": "Những con chó tụ tập quanh Bồ-tát.",
          "lines": [ { "speaker": "CHO_DAU_DAN", "text": "Xin ngài cứu chúng con!" } ]
        }
      ]
    }
  ]
}
```

## Quy tắc
- `lines` rỗng `[]` = **Không thoại** (caption sẽ tự in "THOẠI: Không thoại").
- `speaker` phải trùng `characters[].id`. Lời dẫn dùng nhân vật có `role` = `"Lời dẫn"` (id thường là `NARRATOR`).
- Lời dẫn (narrator) **không** in đỏ như thoại nhân vật trong ảnh storyboard: caption ghi `LỜI DẪN:` màu xám đậm
  để AI video không tạo khẩu hình. Chỉ thoại nhân vật mới in **màu đỏ**.
- Tổng số từ của tất cả `lines` trong 1 cảnh: 25–35 từ.
- Mốc `start/end` liên tục, bắt đầu 0.0 và kết thúc 10.0.
- `voice.engine`: `vieneu` (mặc định) hoặc `edge`. Với `edge`: `voice` = `vi-VN-HoaiMyNeural` / `vi-VN-NamMinhNeural`,
  có thể thêm `"rate": "+10%"`, `"pitch": "-5Hz"` để phân biệt nhân vật.
- `speed` (VieNeu): hệ số tốc độ áp dụng sau khi tổng hợp bằng ffmpeg `atempo` (0.8–1.3).
