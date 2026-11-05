# Hướng dẫn Prompt Video (image-to-video)

Dùng ảnh panel `05_storyboard/canh_NN/panel_XX.png` làm **khung hình đầu**, prompt mô tả chuyển động trong 2–3 giây.
Phù hợp Veo, Kling, Hailuo, Runway, Seedance, Pika...

## Cấu trúc 5 lớp (Tối ưu cho 3D Donghua / AI Video Generators)
1. **Nhân vật (Anchor)** — dán nguyên văn Character Anchor.
2. **Hành động & Biểu cảm** — 1 hành động chính, động từ cụ thể, biểu cảm gương mặt (kiếm mi sắc lạnh, khẩu hình khớp câu thoại hoặc im lặng kiên nghị).
3. **Bối cảnh & Kỹ xảo (VFX)** — ánh sáng kiếm khí, sóng xung kích, mây bay, pháp bảo phát quang.
4. **Chuyển động máy quay (Camera Dynamics & Velocity)**:
   - `Slow push-in / Pan right / Pan left`: Quét cảnh và thoại sâu lắng.
   - `Fast push-in / Whip pan / Speed ramping`: Cao trào, xuất chiêu, trúng đòn.
   - `Slow pull-out`: Lùi máy hé lộ bối cảnh hùng vĩ.
   - `Static`: Tĩnh lặng, tôn nghiêm.
5. **Ánh sáng & Phong cách** — Cinematic lighting, Unreal Engine 5 render, ray-tracing, 16:9 Full HD standard (no letterbox, ample headroom).
6. **Âm thanh & Khẩu hình (Lip-sync)**:
   - Có thoại: `The character speaks in Vietnamese with expressive lip sync: "<câu thoại>"` + cảm xúc khẩu hình.
   - Không thoại: `No dialogue, no speech, closed mouth, resolute expression.` + SFX (tiếng kiếm khí, tiếng nổ, tiếng gió).

## Mẫu
```
[CHARACTER ANCHOR] [action, expression change, lip-sync or resolute silence] in [setting short].
Generous headroom, complete head and hairpins fully visible.
Camera: [movement: slow_push_in / fast_push_in / slow_pan_right / pull_out / static], [lens]. Duration: [DUR] seconds.
Lighting & VFX: [mood lighting, glowing magic artifact, energy aura]. Style: [ART STYLE], 16:9 Full HD full frame, consistent with the first frame.
Audio / Lip movement: [Dialogue line with lip-sync OR "No dialogue, no speech, no lip movement, only SFX"].
```

## Quy tắc
- 1 panel = 1 hành động chính; tránh nhồi nhiều sự kiện.
- Không mô tả lại toàn bộ ảnh — tập trung vào **cái gì chuyển động**.
- Lời dẫn (narrator) **không** đưa vào prompt video; nó nằm ở MP3 tạo bằng TTS và ghép trong CapCut.
- Nếu dùng giọng TTS cho thoại nhân vật: ghi `No speech audio; character mouths the line silently in sync` hoặc
  tắt audio của model, sau đó ghép MP3 thoại trong CapCut.
