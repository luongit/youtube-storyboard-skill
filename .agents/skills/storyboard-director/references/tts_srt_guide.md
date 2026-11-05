# Tạo MP3 + SRT lời thoại (CapCut)

## Engine
| Engine | Khi nào | Giọng |
|---|---|---|
| **VieNeu-TTS** (mặc định, `pip install vieneu`, chạy offline trên máy) | Luôn ưu tiên | 25 giọng preset Bắc/Trung/Nam (xem dưới) |
| **edge-tts** (dự phòng, cần Internet) | VieNeu lỗi hoặc `engine: "edge"` | `vi-VN-NamMinhNeural` (nam), `vi-VN-HoaiMyNeural` (nữ) + `rate`/`pitch` |

## Giọng VieNeu-TTS có sẵn (`--list-voices` để xem lại)
| Giọng | Giới · Vùng · Phong cách | Gợi ý vai |
|---|---|---|
| Thiện Minh | Nam · Bắc · kể chuyện | Người dẫn chuyện, nhà sư |
| Thanh Bình | Nam · Bắc · kể chuyện | Người dẫn chuyện trầm |
| Thiền Tâm Đức | Nam · Bắc · kể chuyện | Bồ-tát, thiền sư, ông lão |
| Hải Đăng | Nam · Bắc · tự nhiên | Thanh niên |
| Quốc Tuấn / Xuân Vĩnh / Phạm Tuyên | Nam · Bắc · tự nhiên | Nam trung niên, vua quan |
| Adam bựa | Nam · Bắc · tự nhiên | Nhân vật hài hước |
| Minh Đức | Nam · Bắc · tin tức | Sứ giả, lính truyền lệnh |
| Quang Sơn | Nam · Trung · tự nhiên | Nhân vật miền Trung |
| Thái Sơn / Đức Trí | Nam · Nam · kể/đọc truyện | Người dẫn giọng Nam |
| Adam / Minh Triết | Nam · Nam | Nhân vật miền Nam |
| Ngọc Linh / Quỳnh Anh | Nữ · Bắc · kể/đọc truyện | Người dẫn nữ |
| Trúc Ly / Đoan Trang / Ngọc Huyền | Nữ · Bắc · tự nhiên | Cô gái, mẹ, công chúa |
| Mai Anh | Nữ · Bắc · tin tức | Nhân vật nghiêm |
| Ngọc Trân | Nữ · Trung · tự nhiên | Nhân vật miền Trung |
| Mỹ Duyên / Kim Thanh / Thục Đoan / Thùy Dung | Nữ · Nam | Nhân vật nữ miền Nam |

Mẹo cho vai trẻ em / con vật: chọn giọng nữ tự nhiên + `"speed": 1.1`; vai già: giọng kể chuyện + `"speed": 0.9`.
Gán giọng trong `characters[].voice` của `script.json` và **chốt với người dùng** ở cuối Giai đoạn 1.

## Lệnh
```powershell
# Toàn bộ dự án
.\.venv\Scripts\python.exe .agents\skills\storyboard-director\scripts\dialogue_tts_srt.py --project projects/<slug>
# Một cảnh
... --project projects/<slug> --scene 3
# Ép dùng edge-tts cho mọi nhân vật
... --project projects/<slug> --engine edge
# Nghe thử 1 giọng
... --preview "Thiện Minh" --text "Xin chào các bạn"
```

## Cách căn thời gian
- Mỗi câu trong panel bắt đầu tại `panel.start` (+0.1s). Nếu câu trước chưa nói xong → đẩy lùi, cách 0.15s.
- Mỗi cảnh được đệm/cắt đúng **10.000s** → cảnh N trong file tổng bắt đầu ở giây (N−1)×10.
- Nếu tổng lời nói của cảnh > 10s → script **cảnh báo** (không cắt mất lời); hãy rút gọn câu và chạy lại.
- Cache theo nội dung (giọng + câu) trong `audio/.cache/` → sửa 1 câu chỉ tổng hợp lại câu đó.

## Đầu ra trong `projects/<slug>/audio/`
| File | Dùng trong CapCut |
|---|---|
| `full_voiceover.mp3` + `full_subtitles.srt` | Kéo vào timeline từ 0:00 → khớp toàn bộ video (N × 10s) |
| `full_subtitles_speaker.srt` | Phụ đề có tên nhân vật đầu dòng (`AN: ...`) |
| `scenes/canh_NN.mp3` + `canh_NN.srt` | Ghép từng cảnh riêng |
| `lines/canh_NN_pXX_<SPEAKER>.mp3` | Từng câu thoại rời (để chỉnh tay / lip-sync) |
| `timing_report.md` | Mốc thời gian, cảnh báo vượt thời lượng |

CapCut: *Nhập* → kéo MP3 vào track âm thanh; *Văn bản → Nhập phụ đề* (hoặc kéo file `.srt`) để tạo phụ đề.
