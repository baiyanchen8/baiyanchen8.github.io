import os
import json
from datetime import datetime

# 設定資料夾路徑
IMAGES_DIR = "asserts/images"
POSTS_DIR = "posts"
JSON_FILE = "asserts/file-list.json"

def generate_file_list():
    # 初始化 JSON 資料結構
    file_list = {
        "images": [],
        "posts": []
    }

    # 處理圖片
    if os.path.exists(IMAGES_DIR):
        for file_name in os.listdir(IMAGES_DIR):
            if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg')):
                file_path = os.path.join(IMAGES_DIR, file_name)
                file_list["images"].append({
                    "path": file_path.replace("\\", "/"),  # 路徑格式化
                    "updated_at": os.path.getmtime(file_path)  # 取得最後修改時間
                })

    # 處理文章
    if os.path.exists(POSTS_DIR):
        for file_name in os.listdir(POSTS_DIR):
            if file_name.lower().endswith('.html'):  # 只處理 HTML 文章
                file_path = os.path.join(POSTS_DIR, file_name)
                file_list["posts"].append({
                    "title": file_name.replace(".html", ""),  # 預設以檔名為標題
                    "path": file_path.replace("\\", "/"),
                    "updated_at": os.path.getmtime(file_path)
                })

    # 將更新時間轉換成人類可讀的格式
    for section in ["images", "posts"]:
        for item in file_list[section]:
            item["updated_at"] = datetime.fromtimestamp(item["updated_at"]).strftime('%Y-%m-%d %H:%M:%S')

    return file_list

def update_json():
    # 生成檔案清單
    file_list = generate_file_list()

    # 寫入或更新 JSON 檔案
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(file_list, f, indent=4, ensure_ascii=False)
    print(f"已更新 JSON 檔案：{JSON_FILE}")

if __name__ == "__main__":
    update_json()
