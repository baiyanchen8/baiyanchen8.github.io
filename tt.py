import markdown
from pathlib import Path

# 指定資料夾
input_dir = Path("posts/md")
output_dir = Path("posts/html")

# 確保輸出資料夾存在
output_dir.mkdir(exist_ok=True)

# 處理每個 Markdown 檔案
for markdown_file in input_dir.glob("*.md"):
    with open(markdown_file, "r", encoding="utf-8") as file:
        markdown_text = file.read()

    # 轉換為 HTML
    html_content = markdown.markdown(
        markdown_text,
        extensions=[
            'markdown.extensions.tables',
            'markdown.extensions.fenced_code',
            'markdown.extensions.codehilite',
            'markdown.extensions.extra',
        ]
    )

    # 生成 HTML
    output_file = output_dir / f"{markdown_file.stem}.html"
    math_config='''{
                tex2jax: {{
                    inlineMath: [['$', '$'], ['\\(', '\\)']],
                    displayMath: [['$$', '$$'], ['\\[', '\\]']],
                    processEscapes: true,
                }},
                "HTML-CSS": {{ availableFonts: ["TeX"] }}
            }'''
    html_template = f"""
    <!DOCTYPE html>
    <html lang="zh-TW">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{markdown_file.stem}</title>
        <link rel="stylesheet" href="../../style.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.5.1/styles/default.min.css">
        <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.5.1/highlight.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML"></script>
        <script type="text/x-mathjax-config">
            MathJax.Hub.Config({math_config}));
        </script>
        <script>hljs.highlightAll();</script>
    </head>
    <body>
        <header><h1>{markdown_file.stem}</h1></header>
        <section>{html_content}</section>
        <footer><p><a href="../../index.html">回首頁</a></p></footer>
    </body>
    </html>
    """

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(html_template)

    print(f"已轉換：{markdown_file.name} -> {output_file.name}")
