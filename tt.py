import markdown
from pathlib import Path

# 指定資料夾
input_dir = Path("posts/md")  # Markdown 檔案所在的資料夾
output_dir = Path("posts/html")  # HTML 檔案的輸出資料夾

# 確保輸出資料夾存在
output_dir.mkdir(exist_ok=True)

# 處理每個 .md 檔案
for markdown_file in input_dir.glob("*.md"):
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

    # 手動處理 LaTeX 公式包裝
    html_content = html_content.replace('$', '<span class="math">$').replace('$', '</span>')
    html_content = html_content.replace('$$', '<div class="math">').replace('$$', '</div>')

    # 生成對應的 HTML 檔案名稱
    output_file = output_dir / f"{markdown_file.stem}.html"

    # MathJax 配置
    math_config = '''{
        tex2jax: {
            inlineMath: [['$', '$'], ['\\(', '\\)']],
            displayMath: [['$$', '$$'], ['\\[', '\\]']],
            processEscapes: true,
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
        <link rel="stylesheet" href="../../style.css">
        <!-- MathJax 用來渲染 LaTeX 公式 -->
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
            <!-- 插入 Markdown 轉換後的 HTML -->
            {html_content}
        </section>

        <footer>
            <p><a href="../index.html">回首頁</a></p>
        </footer>
    </body>
    </html>
    """

    # 將 HTML 寫入檔案
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(html_template)

    print(f"已轉換：{markdown_file.name} -> {output_file.name}")
