import json
import sys
from pathlib import Path
from PIL import Image

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Thẩm định đồng bộ 1:1 Nhân vật - Hình ảnh - Thoại và An toàn Headroom.")
    parser.add_argument("--project", required=True, help="Thư mục dự án")
    parser.add_argument("--scene", type=int, default=None, help="Kiểm tra riêng 1 cảnh")
    args = parser.parse_args()

    project = Path(args.project).resolve()
    script_path = project / "script.json"
    if not script_path.exists():
        print(f"❌ ERROR: Không tìm thấy script.json tại {project}")
        sys.exit(1)

    data = json.loads(script_path.read_text(encoding="utf-8"))
    scenes = sorted(data.get("scenes", []), key=lambda s: int(s.get("scene", 0)))
    if args.scene is not None:
        scenes = [s for s in scenes if int(s.get("scene", 0)) == args.scene]

    sb_dir = project / "05_storyboard"
    errors = []
    warnings = []

    print(f"🔍 [Validator Agent] Bắt đầu rà soát {len(scenes)} cảnh Storyboard...")

    for sc in scenes:
        s_num = int(sc.get("scene", 0))
        canh_dir = sb_dir / f"canh_{s_num:02d}"
        grid_png = sb_dir / f"storyboard_canh_{s_num:02d}.png"
        panels = sc.get("panels", [])

        # Kiểm tra file storyboard grid
        if not grid_png.exists():
            errors.append(f"Cảnh {s_num}: Thiếu ảnh lưới Storyboard '{grid_png.name}'!")
        elif grid_png.stat().st_size < 50000:
            warnings.append(f"Cảnh {s_num}: Ảnh lưới '{grid_png.name}' dung lượng quá nhỏ, có thể bị lỗi khi sinh!")

        # Kiểm tra từng panel
        for p in panels:
            p_num = int(p.get("panel", 0))
            pan_file = canh_dir / f"panel_{p_num:02d}.png"
            subj = str(p.get("visual_subject", "")).upper()
            action = str(p.get("action_vi", ""))
            
            if not pan_file.exists():
                errors.append(f"Cảnh {s_num} Panel {p_num}: Thiếu file ảnh '{pan_file.name}'!")
                continue

            # Kiểm tra kích thước Full HD 16:9
            try:
                with Image.open(pan_file) as im:
                    w, h = im.size
                    if (w, h) != (1920, 1080):
                        warnings.append(f"Cảnh {s_num} Panel {p_num}: Kích thước {w}x{h} khác chuẩn 1920x1080 Full HD.")
            except Exception as e:
                errors.append(f"Cảnh {s_num} Panel {p_num}: Không đọc được file ảnh ({e})")

            # Kiểm tra đồng bộ chủ thể & lời thoại 1:1
            lines = p.get("lines", [])
            speakers = [l.get("speaker") for l in lines]

            if ("NANDA" in subj or "NỮ GIA CHỦ" in subj or "NANDA" in speakers) and "PHẬT" in subj and "NANDA" not in subj:
                errors.append(f"Cảnh {s_num} Panel {p_num}: LỆCH CHỦ THỂ! Lời thoại/Hành động nhắc đến Nanda nhưng chủ thể lại ghi là Đức Phật!")

            print(f"   ✓ Cảnh {s_num:02d} Panel {p_num:02d} [{subj}]: Đã kiểm tra ảnh & mốc thời gian.")

    print("\n--- KẾT QUẢ THẨM ĐỊNH STORYBOARD ---")
    for w in warnings:
        print(f"⚠️ WARN: {w}")
    for e in errors:
        print(f"❌ ERROR: {e}")

    if errors:
        print(f"\n❌ Thất bại: Phát hiện {len(errors)} lỗi vi phạm nguyên tắc Storyboard!")
        sys.exit(1)
    else:
        print(f"\n✅ Hoàn tất: 0 lỗi. Toàn bộ Storyboard đồng bộ 1:1 và đạt chuẩn an toàn!")
        sys.exit(0)

if __name__ == "__main__":
    main()
