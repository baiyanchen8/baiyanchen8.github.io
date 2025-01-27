import markdown
from pathlib import Path

# 指定資料夾
input_dir = Path("md")  # Markdown 檔案所在的資料夾
output_dir = Path("posts")     # HTML 檔案的輸出資料夾

# 確保輸出資料夾存在
output_dir.mkdir(exist_ok=True)

# 處理每個 .md 檔案
for markdown_file in input_dir.glob("*.md"):
    # 讀取 Markdown 檔案內容
    with open(markdown_file, "r", encoding="utf-8") as file:
        markdown_text = file.read()

    # 轉換為 HTML
    html_content = markdown.markdown(markdown_text)

    # 生成對應的 HTML 檔案名稱
    output_file = output_dir / f"{markdown_file.stem}.html"

    html_template = f"""
    <!DOCTYPE html>
    <html lang="zh-TW">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Markdown 轉 HTML</title>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 20px; }}
            h1, h2, h3 {{ color: #333; }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """

    # 將 HTML 寫入檔案
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(html_template)

    print(f"已轉換：{markdown_file.name} -> {output_file.name}")
