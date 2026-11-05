import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Thẩm định tính nhất quán nhân vật, đạo cụ và bối cảnh.")
    parser.add_argument("--project", required=True, help="Thư mục dự án")
    args = parser.parse_args()

    project = Path(args.project).resolve()
    script_path = project / "script.json"
    if not script_path.exists():
        print(f"❌ ERROR: Không tìm thấy script.json tại {project}")
        sys.exit(1)

    data = json.loads(script_path.read_text(encoding="utf-8"))
    characters = data.get("characters", [])
    
    errors = []
    warnings = []

    print(f"🔍 [Validator Agent] Đang thẩm định {len(characters)} nhân vật...")
    for c in characters:
        cid = c.get("id")
        name = c.get("name")
        # Check ref_dir
        if c.get("ref_dir"):
            ref_dir = Path(c["ref_dir"])
            if not ref_dir.is_dir():
                errors.append(f"Nhân vật {cid} ({name}): Thư mục ảnh mẫu ref_dir '{ref_dir}' không tồn tại!")
            else:
                exts = {".jpg", ".jpeg", ".png", ".jfif", ".webp"}
                imgs = [f for f in ref_dir.iterdir() if f.is_file() and f.suffix.lower() in exts]
                if not imgs:
                    errors.append(f"Nhân vật {cid} ({name}): Thư mục '{ref_dir}' không có ảnh mẫu nào!")
                else:
                    print(f"   Nhân vật có ảnh mẫu gốc: {cid} ({len(imgs)} ảnh chuẩn)")
        else:
            if not c.get("anchor_en") and cid != "NARRATOR":
                warnings.append(f"Nhân vật {cid} ({name}): Chưa có anchor_en định vị tạo hình!")
            else:
                print(f"   Nhân vật tạo hình phụ: {cid}")

    # Check document files
    for doc in ["02_nhan_vat.md", "03_phu_kien.md", "04_boi_canh.md"]:
        p = project / doc
        if not p.exists():
            warnings.append(f"Chưa tạo file tài liệu thiết kế: {doc}")

    print("\n--- KẾT QUẢ THẨM ĐỊNH TẠO HÌNH ---")
    for w in warnings:
        print(f"⚠️ WARN: {w}")
    for e in errors:
        print(f"❌ ERROR: {e}")

    if errors:
        print(f"\n Thất bại: Có {len(errors)} lỗi cần khắc phục.")
        sys.exit(1)
    else:
        print(f"\n Hoàn tất: 0 lỗi. Tạo hình nhân vật & bối cảnh hợp lệ!")
        sys.exit(0)

if __name__ == "__main__":
    main()
