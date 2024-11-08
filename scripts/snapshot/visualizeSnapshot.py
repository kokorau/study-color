import json
import os
from PIL import Image
import matplotlib.pyplot as plt

# カラーパレットJSONファイルのパス
PALETTES_JSON_FILE = "../../data/results/color_palettes.json"
# スクリーンショットの保存先ディレクトリ
SCREENSHOTS_DIR = "../../data/screenshots/"


def load_palettes(file_path=PALETTES_JSON_FILE):
    """カラーパレットJSONファイルを読み込み"""
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"{file_path} not found.")
        return []
    except json.JSONDecodeError:
        print("Error decoding JSON.")
        return []


def visualize_palettes_with_images(palettes):
    """画像とカラーパレットを可視化"""
    fig, ax = plt.subplots(len(palettes), 2, figsize=(10, len(palettes) * 2))
    if len(palettes) == 1:
        ax = [ax]  # 1行のみの場合もリストとして扱う

    for i, entry in enumerate(palettes):
        url = entry["url"]
        palette = entry["palette"]

        # スクリーンショット画像のファイルパス
        image_path = f"{SCREENSHOTS_DIR}{url.replace('https://', '').replace('http://', '').replace('/', '_')}.png"

        # 画像を表示
        if os.path.exists(image_path):
            image = Image.open(image_path)
            ax[i][0].imshow(image)
            ax[i][0].axis('off')
        else:
            print(f"Image not found for {url}")
            ax[i][0].text(0.5, 0.5, "Image Not Found", ha='center', va='center', fontsize=12)
            ax[i][0].axis('off')

        # カラーパレットの四角形を描画
        for j, hex_color in enumerate(palette):
            ax[i][1].add_patch(plt.Rectangle((j, 0), 1, 1, color=hex_color))

        # URLラベルを追加
        ax[i][1].text(len(palette) + 0.5, 0.5, url, va='center', fontsize=10)

        # カラーパレットの軸設定
        ax[i][1].set_xlim(0, len(palette))
        ax[i][1].set_ylim(0, 1)
        ax[i][1].axis('off')

    plt.tight_layout()
    plt.show()


def main():
    palettes = load_palettes()
    if palettes:
        visualize_palettes_with_images(palettes)
    else:
        print("No palettes found in JSON file.")


if __name__ == "__main__":
    main()
