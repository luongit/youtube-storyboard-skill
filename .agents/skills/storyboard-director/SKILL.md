---
name: storyboard-director
description: >-
  Đạo diễn Tổng thể & Điều phối Studio Sản xuất Storyboard & Animation (16:9 Full HD). Điều phối quy trình
  khép kín theo mô hình Dual-Agent (Agent Sáng tạo song hành cùng Agent Thẩm định tự động sửa lỗi).
  Quản lý 2 tầng sản xuất: Tầng 1 cốt lõi (Kịch bản, Thiết kế tạo hình, Vẽ & Ghép lưới Storyboard)
  và Tầng 2 tùy chọn (Lồng tiếng AI VieNeu-TTS Voice Cloning & Dựng video Ken Burns Full HD).
---

# 🎬 STUDIO STORYBOARD & ANIMATION DIRECTOR (MASTER COORDINATOR)

## 1. Vai trò & Cơ chế Điều phối Kép (Dual-Agent Studio Pattern)
Skill này đóng vai trò là **Tổng Đạo Diễn (Studio Executive Director)**, điều phối chuỗi 5 micro-skills chuyên biệt theo quy trình chuẩn studio hoạt hình:
1. Mỗi công đoạn luôn có **2 Agent chạy song song**:
   - **Agent Thực thi (Creator / Designer Agent):** Đọc suy luận cốt truyện, lên kịch bản, thiết kế tạo hình, vẽ panel, tạo âm thanh hoặc render video.
   - **Agent Thẩm định (Auditor / Validator Agent):** Chạy công cụ kiểm tra tự động, rà soát đối chiếu chéo theo các nguyên tắc cốt tử (Đồng bộ 1:1, Bảo toàn Headroom không mất đầu, Chuẩn 1920x1080 Full HD, Nhịp nói 2.5–3.3 từ/s) và **TỰ ĐỘNG CHỈNH SỬA LỖI** trước khi trình kết quả cho người dùng.
2. Quy trình phân thành **2 tầng rõ rệt**:
   - **TẦNG 1: BỘ STORYBOARD CỐT LÕI (Bắt buộc):** Hoàn thiện kịch bản, tạo hình và bộ ảnh Storyboard dạng lưới có caption, tự động xuất `voice-script.md` chữ thường (không in hoa).
   - **TẦNG 2: SẢN XUẤT ĐA PHƯƠNG TIỆN (Tùy chọn):** Tạo giọng đọc AI clone và dựng video animation.

---

## 2. Nguyên Tắc Cốt Tử Toàn Hệ Thống (Studio Cardinal Rules)
1. **Bám sát Cốt truyện 100% (Faithful Narrative Adaptation):**
   - Tuyệt đối không cắt xén, không lược bỏ tình tiết cốt tủy của bản kinh gốc. Câu chuyện mở rộng tuần tự đầy đủ các hồi tiền kiếp và hiện tại.
2. **Thời Lượng Cảnh Tối Đa 10.0 Giây (≤ 10.0s):**
   - Số lượng cảnh được quyết định tự nhiên bởi chiều sâu cốt truyện (có thể 16, 20, 24 cảnh hoặc hơn), nhưng thời lượng mỗi cảnh **tuyệt đối không vượt quá 10.0s** (ví dụ: Panel 1: 5.0s, Panel 2: 5.0s; hoặc 4s + 6s) nhằm giữ nhịp hoạt hình cô đọng, dứt khoát.
3. **Phong Cách Phim Hoạt Hình Đầy Đủ Thoại & Tương Tác (Mẫu `assets/mp4_template`):**
   - Đẩy mạnh các đoạn hội thoại đối đáp trực tiếp (`dialogue`) giữa các nhân vật với đầy đủ cảm xúc, cử chỉ, chuyển góc máy (shot-reverse-shot) sinh động như phim hoạt hình mẫu.
   - Lời dẫn (`NARRATOR`) chỉ là cầu nối chuyển tiếp; linh hồn câu chuyện nằm ở hành động và lời thoại của chính các nhân vật.
4. **Đồng Bộ 1:1 Tuyệt Đối:**
   - Nhân vật nào nói thì hình ảnh panel phải thể hiện đúng nhân vật đó. Khóa 100% ảnh Phật gốc do người dùng cung cấp (`assets/images/Buddha/`).
5. **Bảo Toàn Headroom An Toàn (Headroom Safety):**
   - Mọi khung hình đều phải có khoảng thở an toàn phía trên đầu, tuyệt đối không cắt cụt đầu, búi tóc, mũ miện hay hào quang.
6. **Chuẩn Full HD 16:9 Tràn Viền:**
   - Xuất hình ảnh và video chuẩn 1920x1080 tràn khung, không dùng dải đen letterbox.
7. **Tự Động Xuất `voice-script.md` (Viết thường 100%):**
   - Sau khi tạo xong Storyboard, tự động tổng hợp toàn bộ lời thoại và lời dẫn thành file `voice-script.md` viết hoàn toàn bằng chữ thường (không in hoa).
8. **Quy Cách Prompt Storyboard Đơn Khối (Single-Block Prompt):**
   - Mỗi cảnh được đóng gói thành **MỘT KHỐI CODE DUY NHẤT (` ```text `)** chứa đầy đủ: Tiêu đề cảnh (thời lượng ≤ 10s), Địa điểm & Chủ thể (kèm ghi chú "Tham chiếu ảnh đính kèm"), Tone cảm xúc, Bối cảnh tổng quan, Chi tiết từng Panel (thời gian, góc máy, lời dẫn, lời thoại, hành động) và Bối cảnh chung (Prompt tiếng Anh hoàn chỉnh). Người dùng chỉ cần copy 1 khối, đính kèm ảnh và dán thẳng vào AI tạo ảnh.
9. **Cấu Trúc Thư Mục Chuẩn Hóa:**
   - `inputs/`: Chứa file kinh văn gốc (`.md`).
   - `inputs/assets/`: Chứa toàn bộ tài nguyên tham chiếu do người dùng cung cấp (`Nhân vật/`, `Bối cảnh/`, `Phụ kiện/`, `voices/`, `mp3-template/`).
   - `runtime/`: Chứa toàn bộ script Python trung gian/xử lý tự động (được cấu hình trong `.gitignore`, không đưa lên Git).
   - `outputs/`: Chứa toàn bộ sản phẩm hoàn thiện (`01_kich_ban.md`, `05_storyboard/`, `05_prompts_tao_anh.md`, `voice-script.md`).

---

## 3. Hệ Thống 5 Micro-Skills Thành Viên

```
.agents/skills/
├── script-director/          # [Skill 1] Kịch bản & Phân cảnh tuần tự (Core)
├── concept-designer/         # [Skill 2] Tạo hình nhân vật, đạo cụ, bối cảnh & Bảo toàn ảnh gốc (Core)
├── storyboard-artist/        # [Skill 3] Vẽ panel & Ghép lưới Storyboard Caption (Core Milestone)
├── voice-audio-engineer/     # [Skill 4] Lồng tiếng AI VieNeu-TTS Voice Cloning & SRT (Optional)
└── video-animator/           # [Skill 5] Ken Burns Video 1080p & Master Video (Optional)
```

| STT | Skill | Phân loại | Công cụ Thẩm định (Validator Agent) | Đầu ra chính |
|:---:|---|:---:|---|---|
| **1** | `script-director` | **Cốt lõi** | `scripts/validate_script.py` (0 lỗi từ ngữ, mốc thời gian) | `01_kich_ban.md`, `script.json` |
| **2** | `concept-designer` | **Cốt lõi** | `scripts/verify_character_consistency.py` (Khóa ảnh gốc, 5 góc) | `02_nhan_vat.md`, `refs/` |
| **3** | `storyboard-artist` | **Cốt lõi** | `scripts/verify_panel_alignment.py` (Khóa Headroom, 1:1 sync) | `05_storyboard/storyboard_canh_NN.png`, `voice-script.md` |
| **4** | `voice-audio-engineer` | *Tùy chọn* | `scripts/verify_audio_sync.py` (Khớp timeline, subtitle SRT) | `audio/scenes/canh_NN.mp3`, `full_voiceover.mp3` |
| **5** | `video-animator` | *Tùy chọn* | `scripts/verify_video_output.py` (Full HD 1080p, không viền đen) | `videos/full_video.mp4` |

---

## 3. Quy Trình Sản Xuất Tuần Tự & Điểm Dừng (Checkpoints)

### GIAI ĐOẠN 1: TẦNG CỐT LÕI (CORE STORYBOARD)
1. **Bước 1 — Biên kịch (`script-director`):**
   - Đọc `inputs/<tên_truyen>.md`.
   - Phân tích nhịp cảm xúc, phân cảnh linh hoạt theo câu chuyện (không giới hạn cứng 10s).
   - Agent thẩm định chạy `validate_script.py` sửa hết lỗi nhịp nói và mốc thời gian.
   - Xuất `01_kich_ban.md` và hỏi người dùng: *"Chốt kịch bản?"*.
2. **Bước 2 — Tạo hình (`concept-designer`):**
   - Nạp ảnh mẫu người dùng cung cấp (Buddha trong `assets/images/Buddha`).
   - Thiết kế character sheet 5 góc nhìn nền trắng cho nhân vật phụ (Nanda, Chư Tăng).
   - Agent thẩm định chạy `verify_character_consistency.py` khóa chặt tính nhất quán.
   - Xuất `02_nhan_vat.md`, `refs/` và hỏi người dùng: *"Chốt nhân vật & bối cảnh?"*.
3. **Bước 3 — Vẽ Storyboard & Xuất Voice Script (`storyboard-artist`):**
   - Sinh ảnh từng panel Full HD 16:9, neo crop an toàn `centering=(0.5, 0.10)` bảo vệ khoảng thở trên đầu (Headroom Safe).
   - Ghép lưới thích ứng (Adaptive Grid Layout: 2x1, 3x1, 2x2...) kèm caption đen (hành động) và đỏ (lời thoại).
   - Agent thẩm định chạy `verify_panel_alignment.py` kiểm tra chéo 1:1, tự động loại trừ mọi trường hợp gán sai ảnh nhân vật.
   - **Tự động xuất `voice-script.md`:** Chạy `generate_voice_script.py` tổng hợp toàn bộ câu thoại và lời dẫn từ tất cả các cảnh thành file `outputs/<tên_dự_án>/voice-script.md` với quy cách **100% chữ thường (không in hoa)**.
   - **🏁 MILESTONE HOÀN TẤT TẦNG 1:** Trình ảnh Storyboard và file `voice-script.md` cho người dùng và hỏi:
     *"Bộ Storyboard tĩnh và kịch bản giọng đọc `voice-script.md` đã hoàn thành trọn vẹn và đạt chuẩn 100%. Bạn có muốn tiếp tục bước sang khâu Lồng tiếng AI và Dựng video không?"*

---

### GIAI ĐOẠN 2: TẦNG ĐA PHƯƠNG TIỆN (TÙY CHỌN KHI CẦN LÀM VIDEO)
4. **Bước 4 — Lồng tiếng AI (`voice-audio-engineer`):**
   - Áp dụng VieNeu-TTS Zero-shot Voice Cloning trích xuất từ các file mẫu MP3 của người dùng (`assets/mp3-template/`).
   - Ghép mốc thời gian câu thoại, xuất file MP3 từng cảnh và phụ đề `.srt` chính xác cho CapCut.
   - Agent thẩm định chạy `verify_audio_sync.py` đối soát khớp nhịp.
5. **Bước 5 — Dựng Video Master (`video-animator`):**
   - Render hiệu ứng chuyển động máy quay FFmpeg Ken Burns có neo trục Y chống mất đầu nhân vật.
   - Ghép đồng bộ âm thanh thoại và nhạc thiền.
   - Ghép nối thành video master hoàn chỉnh chuẩn Full HD 1080p, tràn viền không viền đen.
   - Agent thẩm định chạy `verify_video_output.py` kiểm tra thông số video trước khi bàn giao.

---

## 4. Các Lệnh Nhanh Điều Phối

| Lệnh | Ý nghĩa | Skill được gọi |
|---|---|---|
| `Tạo kịch bản` | Biên kịch & Thẩm định kịch bản 0 lỗi | `script-director` |
| `Thiết kế nhân vật` | Tạo hình & Quản lý thư viện ảnh gốc | `concept-designer` |
| `Vẽ storyboard cảnh N` | Vẽ panel & Ghép lưới Storyboard | `storyboard-artist` |
| `Tạo audio` | Lồng tiếng AI VieNeu-TTS & Xuất SRT | `voice-audio-engineer` |
| `Dựng video cảnh N` / `Dựng full video` | Render video animatic Ken Burns | `video-animator` |
| `Chạy trọn gói` | Thực hiện tuần tự cả 5 bước khép kín | `storyboard-director` (Master) |
