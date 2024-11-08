import json
import os
from sklearn.cluster import KMeans
from PIL import Image
import numpy as np
from scripts.common.color import Srgb  # カラーモデルのクラスをインポート

# 定数の設定
SCREENSHOTS_DIR = "../../data/screenshots/"  # スクリーンショットの保存先ディレクトリ
OUTPUT_JSON_FILE = "../../data/results/color_palettes.json"  # 出力するJSONファイルのパス
URLS_FILE = "../../data/raw/website.json"  # URLリストが保存されたJSONファイル
INITIAL_CLUSTER_COUNT = 10  # 初期のKMeansクラスター数
FINAL_PALETTE_SIZE = 4  # 最終的なカラーパレットの色数

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

def extract_palette(image_path, initial_clusters=INITIAL_CLUSTER_COUNT, final_colors=FINAL_PALETTE_SIZE):
    """画像からKMeansで多めにクラスターを作成し、上位の色を選んでHex形式で返す"""
    image = Image.open(image_path)
    image = image.resize((100, 100))  # 計算負荷を下げるためにサイズを縮小
    image_np = np.array(image)
    image_np = image_np.reshape(-1, 3)  # ピクセル単位で色を配列に変換

    # KMeansで多めのクラスターで色をクラスタリング
    kmeans = KMeans(n_clusters=initial_clusters, random_state=0).fit(image_np)
    colors = kmeans.cluster_centers_
    labels = kmeans.labels_

    # クラスターごとのピクセル数（比重）を取得し、重い順に並べ替え
    counts = np.bincount(labels)
    sorted_indices = np.argsort(-counts)[:final_colors]  # 上位の色インデックスを選択

    # 色をHexに変換し、上位の色を取得
    palette = [Srgb(colors[i][0] / 255, colors[i][1] / 255, colors[i][2] / 255).to_hex().hex_value for i in sorted_indices]
    return palette

def analyze_images(urls):
    """取得したスクリーンショットのカラーパレットを分析してJSONに保存"""
    results = []

    for url in urls:
        # ファイル名の生成
        filename = f"{SCREENSHOTS_DIR}{url.replace('https://', '').replace('http://', '').replace('/', '_')}.png"

        if os.path.exists(filename):
            try:
                palette = extract_palette(filename)
                results.append({"url": url, "palette": palette})
                print(f"Palette extracted for {url}")
            except Exception as e:
                print(f"Error extracting palette for {url}: {e}")
        else:
            print(f"Screenshot not found for {url}")

    # 結果をJSONに保存
    with open(OUTPUT_JSON_FILE, 'w') as outfile:
        json.dump(results, outfile, indent=4)
    print(f"Results saved to {OUTPUT_JSON_FILE}")

def main():
    urls = load_urls()
    if urls:
        analyze_images(urls)
    else:
        print("No URLs found in website.json.")

if __name__ == "__main__":
    main()
