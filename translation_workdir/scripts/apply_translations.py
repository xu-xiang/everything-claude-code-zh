import os
import shutil
import argparse

def main():
    parser = argparse.ArgumentParser(description="将翻译后的文件应用回原目录")
    parser.add_argument("--dry-run", action="store_true", help="只显示将要执行的操作，不实际移动")
    args = parser.parse_args()

    # 扫描所有以 _zh 结尾的目录或文件
    targets = []
    for item in os.listdir("."):
        if item.endswith("_zh") or "_zh.md" in item:
            targets.append(item)

    if not targets:
        print("未发现任何翻译后的目标 (_zh)。")
        return

    print(f"发现以下翻译内容: {targets}")
    
    confirm = "y" if args.dry_run else input("确认要将这些翻译应用回原文件吗？原文件将被覆盖！(y/n): ")
    if confirm.lower() != 'y':
        print("操作已取消。")
        return

    for item in targets:
        if os.path.isdir(item):
            # 处理目录，例如 agents_zh -> agents
            original_dir = item.replace("_zh", "")
            for root, _, files in os.walk(item):
                for f in files:
                    src_file = os.path.join(root, f)
                    rel_path = os.path.relpath(src_file, item)
                    dst_file = os.path.join(original_dir, rel_path)
                    
                    if args.dry_run:
                        print(f"[DRY-RUN] 覆盖: {dst_file}")
                    else:
                        os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                        shutil.move(src_file, dst_file)
            
            if not args.dry_run:
                shutil.rmtree(item)
                print(f"已清理目录: {item}")

        elif os.path.isfile(item) and item.endswith("_zh.md"):
            # 处理根目录文件，例如 README_zh.md -> README.md
            original_file = item.replace("_zh.md", ".md")
            if args.dry_run:
                print(f"[DRY-RUN] 覆盖: {original_file}")
            else:
                shutil.move(item, original_file)
                print(f"已替换文件: {original_file}")

    print("\n应用完成。" if not args.dry_run else "\n模拟运行完成。")

if __name__ == "__main__":
    main()
