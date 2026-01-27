import os
import argparse
import subprocess
import hashlib
import json
import sys

# 注入代理配置
PROXY_CONFIG = {
    "http_proxy": "http://127.0.0.1:8442",
    "https_proxy": "http://127.0.0.1:8442",
    "no_proxy": "localhost,127.0.0.1,::1,127.0.0.0/8,192.168.0.0/16,10.0.0.0/8,172.16.0.0/12"
}

def get_file_hash(file_path):
    with open(file_path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def main():
    os.environ.update(PROXY_CONFIG)
    
    # 定义翻译工作区的基本路径（相对于项目根目录）
    WORKDIR = "translation_workdir"
    CACHE_PATH = os.path.join(WORKDIR, "cache", "translation_db.json")
    DEFAULT_PROMPT = os.path.join(WORKDIR, "prompts", "translate_zh.md")

    parser = argparse.ArgumentParser(description="Gemini CLI 翻译自动化归档工具")
    parser.add_argument("--prompt", default=DEFAULT_PROMPT, help="提示词模板路径")
    parser.add_argument("--limit", type=int, default=None, help="限制处理文件数")
    parser.add_argument("--force", action="store_true", help="强制调用 AI 重译")
    parser.add_argument("--model", default="gemini-3-flash-preview", help="模型名称")
    args = parser.parse_args()

    # 1. 扫描项目中所有的 .md 文件 (排除工作目录本身)
    all_md_files = []
    for root, dirs, files in os.walk("."):
        if any(x in root for x in [WORKDIR, "bak", "node_modules", ".git", "_zh"]):
            continue
        for f in files:
            if f.endswith(".md") and not f.endswith("_zh.md"):
                all_md_files.append(os.path.abspath(os.path.join(root, f)))

    if not os.path.exists(args.prompt):
        print(f"错误: 提示词文件不存在: {args.prompt}")
        return

    with open(args.prompt, 'r') as f:
        prompt_template = f.read()
    
    # 加载翻译指纹数据库
    db = {}
    if os.path.exists(CACHE_PATH):
        try:
            with open(CACHE_PATH, 'r') as f: db = json.load(f)
        except: pass
    
    print(f"\n>>> 发现 {len(all_md_files)} 个 Markdown 待处理文件")

    processed = 0
    restored = 0
    
    for src in all_md_files:
        if args.limit and (processed + restored) >= args.limit: break
        
        rel_from_root = os.path.relpath(src, os.getcwd())
        # 计算 _zh 路径逻辑
        parts = rel_from_root.split(os.sep)
        if len(parts) > 1:
            target_rel_path = os.path.join(f"{parts[0]}_zh", *parts[1:])
        else:
            name, ext = os.path.splitext(parts[0])
            target_rel_path = f"{name}_zh{ext}"
        
        abs_dst = os.path.abspath(target_rel_path)
        os.makedirs(os.path.dirname(abs_dst), exist_ok=True)

        h = get_file_hash(src)
        
        # 恢复逻辑
        if not args.force and src in db and db[src].get("md5") == h:
            translated_content = db[src].get("content")
            if translated_content:
                with open(abs_dst, 'w') as f:
                    f.write(translated_content)
                print(f"[RESTORED] {rel_from_root}")
                restored += 1
                continue

        # 翻译逻辑
        print(f"----------------------------------------------------------------")
        print(f"[{processed + restored + 1}] 翻译中 (AI): {rel_from_root}")
        
        instruction = (
            f"任务：翻译文件 @{src} 并保存为中文。\n"
            f"目标路径：{abs_dst}\n"
            f"提示词指令：\n{prompt_template}"
        )

        cmd = ["gemini", "-m", args.model, "-y", "--allowed-tools", "write_file", "-p", instruction]
        
        try:
            process = subprocess.run(cmd)
            if process.returncode == 0:
                if os.path.exists(abs_dst):
                    with open(abs_dst, 'r') as f:
                        new_content = f.read()
                    db[src] = {"md5": h, "content": new_content}
                    with open(CACHE_PATH, 'w') as f:
                        json.dump(db, f, indent=2)
                    processed += 1
                    print(f">>> [OK] 内容已同步至数据库\n")
            else:
                print(f">>> [ERR] {rel_from_root} (Code: {process.returncode})")
        except Exception as e:
            print(f">>> [EXC] {rel_from_root}: {str(e)}")

    print(f"\n任务结束。恢复: {restored}, 翻译: {processed}")

if __name__ == "__main__":
    main()
