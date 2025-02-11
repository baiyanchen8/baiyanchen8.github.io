import os
import json
import re
from pathlib import Path
from datetime import datetime
import markdown

# 設定資料夾路徑
IMAGES_DIR = "asserts/images"
POSTS_DIR = "posts"
MD_DIR = "md"
JSON_FILE = "asserts/file-list.json"

def generate_file_list():
    """生成 JSON 檔案清單，支援樹狀結構"""
    file_list = {
        "images": [],
        "posts": {}
    }

    # 處理圖片
    for root, _, files in os.walk(IMAGES_DIR):
        for file_name in files:
            if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg')):
                file_path = os.path.join(root, file_name)
                file_list["images"].append({
                    "path": file_path.replace("\\", "/"),  # 路徑格式化
                    "updated_at": datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')  # 轉換為可讀格式
                })

    # 處理文章，按主題分類
    for root, _, files in os.walk(POSTS_DIR):
        for file_name in files:
            if file_name.lower().endswith('.html'):
                file_path = os.path.join(root, file_name).replace("\\", "/")
                
                # 解析主題名稱，例如 "posts/001.game/teteris.html" -> theme = "001.game"
                parts = file_path.split('/')
                if len(parts) >= 3:
                    theme = parts[1]  # 取得主題名稱，例如 "001.game"

                    if theme not in file_list["posts"]:
                        file_list["posts"][theme] = []  # 如果主題不存在，先建立

                    file_list["posts"][theme].append({
                        "title": file_name.replace(".html", ""),  # 以檔名為標題
                        "path": f"/{file_path}",
                        "updated_at": datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
                    })

    return file_list

def update_json():
    """更新 JSON 檔案"""
    file_list = generate_file_list()
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(file_list, f, indent=4, ensure_ascii=False)
    print(f"已更新 JSON 檔案：{JSON_FILE}")

def convert_markdown_to_html():
    """將 Markdown 轉換成 HTML，支援遞迴處理子目錄"""
    input_dir = Path(MD_DIR)
    output_dir = Path(POSTS_DIR)

    # 遞迴遍歷 Markdown 目錄
    for markdown_file in input_dir.rglob("*.md"):
        # 讀取 Markdown 檔案內容
        with open(markdown_file, "r", encoding="utf-8") as file:
            markdown_text = file.read()

        # 使用 Markdown 擴展轉換 HTML
        html_content = markdown.markdown(
            markdown_text,
            extensions=[
                'markdown.extensions.tables',      # 表格
                'markdown.extensions.fenced_code', # 程式碼區塊
                'markdown.extensions.codehilite',  # 程式碼高亮
                'markdown.extensions.extra',       # 額外支援 (如腳註等)
            ]
        )

        # 保留原始的數學公式標記，不進行額外包裝
        html_content = re.sub(
            r'\$\$(.*?)\$\$',  # 區塊公式
            r'$$\1$$',
            html_content,
            flags=re.DOTALL
        )
        html_content = re.sub(
            r'(?<!\$)\$(.+?)\$(?!\$)',  # 行內公式
            r'$\1$',
            html_content
        )

        # 將輸出目錄結構與輸入目錄結構對應
        relative_path = markdown_file.relative_to(input_dir)
        output_file = output_dir / relative_path.with_suffix(".html")
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # MathJax 配置
        math_config = '''{
            tex2jax: {
                inlineMath: [["$", "$"]],
                displayMath: [["$$", "$$"]],
                processEscapes: true,
                skipTags: ["script", "noscript", "style", "textarea", "pre", "code"]
            },
            "HTML-CSS": { availableFonts: ["TeX"] }
        }'''

        # HTML 模板
        html_template = f"""
        <!DOCTYPE html>
        <html lang="zh-TW">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{markdown_file.stem}</title>
            <link rel="stylesheet" href="./style.css">
            <script type="text/javascript" async
                src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML">
            </script>
            <script type="text/x-mathjax-config">
                MathJax.Hub.Config({math_config});
            </script>
        </head>
        <body>
            <header>
                <h1>{markdown_file.stem}</h1>
            </header>
            <section>
                {html_content}
            </section>
            <footer>
                <p><a href="/index.html">回首頁</a></p>
            </footer>
        </body>
        </html>
        """

        # 寫入 HTML 檔案
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(html_template)
        print(f"已轉換：{markdown_file} -> {output_file}")

if __name__ == "__main__":
    print("選擇功能：")
    print("1. 更新 JSON 檔案")
    print("2. 轉換 Markdown 為 HTML")
    choice = input("請輸入選項 (1/2)：")

    if choice == "1":
        update_json()
    elif choice == "2":
        convert_markdown_to_html()
    else:
        print("無效的選項，請重新執行程式！")
