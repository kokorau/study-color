import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from playwright.sync_api import sync_playwright
import sys

# スクリーンショットの保存先ディレクトリ
SCREENSHOTS_DIR = "../../data/screenshots/"
# URLリストが保存されたJSONファイル
URLS_FILE = "../../data/raw/website.json"
# デフォルトの並列数
DEFAULT_CONCURRENCY = 5

# 保存先ディレクトリが存在しない場合は作成
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

def load_urls(file_path=URLS_FILE):
    """website.jsonからURLリストを読み込む"""
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data.get("urls", [])
    except FileNotFoundError:
        print(f"{file_path} not found.")
        return []
    except json.JSONDecodeError:
        print("Error decoding JSON.")
        return []

def capture_screenshot(url):
    """1つのURLのスクリーンショットを取得"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            page = browser.new_page()
            page.goto(url, timeout=60000)  # URLにアクセス

            # ページの読み込み完了を待機
            page.wait_for_load_state("networkidle", timeout=30000)  # ネットワークが静止状態になるまで待機

            # アニメーションが終わるのを待つため5秒待機
            page.wait_for_timeout(5000)

            # URLをファイル名に変換
            filename = f"{SCREENSHOTS_DIR}{url.replace('https://', '').replace('http://', '').replace('/', '_')}.png"

            # ファーストビューのみをキャプチャ
            page.screenshot(path=filename)

            print(f"Captured screenshot for: {url}")
            page.close()
        except Exception as e:
            print(f"Error capturing screenshot for {url}: {e}")
        finally:
            browser.close()

def capture_screenshots_parallel(urls, concurrency=DEFAULT_CONCURRENCY):
    """指定されたURLリストのスクリーンショットを並列に取得"""
    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = {executor.submit(capture_screenshot, url): url for url in urls}
        for future in as_completed(futures):
            url = futures[future]
            try:
                future.result()  # 実行結果を取得してエラーをキャッチ
            except Exception as e:
                print(f"Error capturing screenshot for {url}: {e}")

def main():
    # 並列数の指定（引数があれば使用、無ければデフォルト）
    concurrency = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_CONCURRENCY

    urls = load_urls()
    if urls:
        capture_screenshots_parallel(urls, concurrency)
    else:
        print("No URLs found in website.json.")

if __name__ == "__main__":
    main()
