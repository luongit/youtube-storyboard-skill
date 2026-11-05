# 🎬 YouTube Storyboard & Animation Maker

> **Antigravity Agent Skills Suite** — Bộ công cụ AI Agent tự động chuyển thể cốt truyện, tích truyện kinh điển thành **Storyboard hoạt hình chuẩn điện ảnh 16:9 Full HD** và **Video Animation hoàn chỉnh**.

---

## 🌟 Tính Năng Nổi Bật

- **Mô hình Dual-Agent khép kín:** Mỗi công đoạn đều có *Agent Sáng tạo* song hành cùng *Agent Thẩm định* tự động rà soát, đạt chuẩn **0 lỗi**.
- **Chuẩn hóa nhịp phim hoạt hình:** Thời lượng mỗi cảnh **tối đa 10 giây (≤ 10.0s)** (chuẩn 5s/panel) giúp tiết tấu video cô đọng, cuốn hút.
- **Đồng bộ 1:1 tuyệt đối:** Lời thoại và hành động của nhân vật nào thì hình ảnh panel phải thể hiện chuẩn xác nhân vật đó.
- **Bảo toàn khoảng thở trên đầu (Headroom Safe):** Tự động neo tỷ lệ an toàn, không bao giờ cắt cụt đầu, búi tóc hay vầng hào quang.
- **Bộ Prompt tạo ảnh Đơn khối (Single Code Block):** Mỗi cảnh được đóng gói trong **đúng 1 khối code**, người dùng chỉ cần copy 1 click và dán thẳng vào Midjourney / ChatGPT / Flux / Leonardo.ai.
- **Tự động xuất Voice Script & SRT:** Tự động tổng hợp kịch bản đọc chữ thường 100% để thu âm mượt mà và xuất phụ đề chuẩn cho CapCut / Premiere.

---

## 🏛️ Kiến Trúc 5 Micro-Skills

```
.agents/skills/
├── storyboard-director/      # [Master] Đạo diễn tổng thể & điều phối quy trình
├── script-director/          # [Skill 1] Biên kịch phân cảnh chi tiết (tối đa 10s/cảnh)
├── concept-designer/         # [Skill 2] Khóa tạo hình nhân vật gốc, bối cảnh, đạo cụ
├── storyboard-artist/        # [Skill 3] Xếp lưới Storyboard Full HD & xuất Voice Script
├── voice-audio-engineer/     # [Skill 4] Lồng tiếng AI (VieNeu-TTS Voice Cloning) & SRT
└── video-animator/           # [Skill 5] Render video Ken Burns 1080p không viền đen
```

---

## 🗂️ Cấu Trúc Thư Mục

```
├── inputs/                       # Dữ liệu đầu vào (được .gitignore bảo vệ)
│   ├── <ten_truyen>.md           # Văn bản cốt truyện / kinh văn gốc
│   └── assets/                   # Kho ảnh tham chiếu (Nhân vật, Bối cảnh, Phụ kiện)
├── outputs/                      # Sản phẩm hoàn thiện xuất ra (được .gitignore bảo vệ)
│   └── <ten_du_an>/
│       ├── 01_kich_ban.md        # Kịch bản phân cảnh chi tiết
│       ├── 05_storyboard/        # Ảnh panel 1080p và ảnh lưới Storyboard
│       ├── 05_prompts_tao_anh.md # Trọn bộ 24 Prompt đơn khối copy dùng ngay
│       └── voice-script.md       # Lời thoại chữ thường 100% để thu âm
├── runtime/                      # Script Python trung gian (được .gitignore bảo vệ)
├── .agents/skills/               # Mã nguồn 5 Micro-Skills
├── requirements.txt              # Danh sách thư viện Python
└── README.md                     # Hướng dẫn sử dụng
```

---

## 🚀 Cài Đặt (Khởi Tạo Nhanh)

### Yêu cầu:
- Python 3.10+
- FFmpeg (đã thêm vào PATH)

### Cài đặt môi trường:
```powershell
# 1. Tạo và kích hoạt môi trường ảo
python -m venv .venv
.\.venv\Scripts\Activate.ps1    # Trên Linux/macOS: source .venv/bin/activate

# 2. Cài đặt thư viện phụ thuộc
pip install -r requirements.txt

# 3. Cài đặt FFmpeg (nếu chưa có trên Windows)
winget install Gyan.FFmpeg
```

---

## 💡 Cách Sử Dụng (3 Bước Đơn Giản)

### Bước 1: Chuẩn bị dữ liệu
- Đặt file truyện (`.md`) vào thư mục `inputs/`.
- Đặt các ảnh tham chiếu nhân vật/bối cảnh vào `inputs/assets/`.

### Bước 2: Kích hoạt Agent
Mở Antigravity IDE và nhập câu lệnh:
```text
Dùng skill storyboard-director, hãy chuyển thể cốt truyện trong inputs/<ten_truyen>.md thành Storyboard hoạt hình hoàn chỉnh.
```

### Bước 3: Duyệt và nhận sản phẩm
1. **Duyệt kịch bản:** Agent xuất `01_kich_ban.md` $\rightarrow$ Bạn gõ `"Chốt kịch bản"`.
2. **Duyệt tạo hình:** Agent kiểm tra ảnh tham chiếu $\rightarrow$ Bạn gõ `"Chốt nhân vật"`.
3. **Nhận Storyboard:** Agent xuất ảnh lưới tại `05_storyboard/`, file `05_prompts_tao_anh.md` và `voice-script.md`.
4. *(Tùy chọn)* Nếu muốn dựng video, Agent sẽ tiếp tục lồng tiếng AI và render video Ken Burns 1080p.

---

## 👨‍💻 Tác Giả & Phát Triển

- **Tác giả:** Nguyễn Anh Lương (LuongNA)
- **Website:** [https://lungcode.com/](https://lungcode.com/)
- **Repository:** [https://github.com/luongit/youtube-storyboard-skill](https://github.com/luongit/youtube-storyboard-skill)

---

## 📜 Giấy Phép

Phát triển trên nền tảng **Antigravity Customization Framework**. Mã nguồn mở phục vụ cho mục đích sáng tạo nội dung, giáo dục và làm phim hoạt hình phi thương mại.
