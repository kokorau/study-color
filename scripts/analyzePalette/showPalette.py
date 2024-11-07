import json
import random
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from collections import defaultdict
import scripts.common.color as color

MAX_ITEMS_IN_GROUP = 300


def load_results(file_path):
    """保存された結果データを読み込む関数"""
    with open(file_path, 'r') as f:
        return json.load(f)

def sort_palette_by_saturation(hex_palette):
    """パレット内の色をHSLのSaturationでソート"""
    rgb_palette = [color.Hex(hex_color).to_srgb() for hex_color in hex_palette]
    hsl_palette = [color.Hex(hex_color).to_hsl() for hex_color in hex_palette]
    sorted_palette = sorted(hsl_palette, key=lambda hsl: hsl.l)  # Saturationでソート
    sorted_hex_palette = [hsl.to_hex() for hsl in sorted_palette]
    return sorted_hex_palette

def sort_palettes_by_hue(grouped_palettes):
    """パレットのリストをHueでソート"""

    def calculate_average_hue(hex_palette):
        """パレットの平均Hueを計算"""
        rgb_palette = [color.Hex(hex_color).to_srgb() for hex_color in hex_palette]
        hsl_palette = [color.Hex(hex_color).to_hsl() for hex_color in hex_palette]
        average_lightness = sum(hsl.l for hsl in hsl_palette) / len(hsl_palette)
        return average_lightness

    # パターンごとにパレットをHueでソート
    for pattern, palettes in grouped_palettes.items():
        grouped_palettes[pattern] = sorted(palettes, key=calculate_average_hue)


def plot_grouped_palettes(grouped_palettes, title, max_items=MAX_ITEMS_IN_GROUP, palette_gap=0.5, items_per_row=10):
    """グループ化されたカラーパレットをまとめて表示する関数"""
    # 各パターンごとにサブプロットを作成
    num_patterns = len(grouped_palettes)
    fig, axs = plt.subplots(num_patterns, 1, figsize=(12, 3 * num_patterns))

    for ax, (pattern, palettes) in zip(axs, grouped_palettes.items()):
        # ランダムに最大max_items個のパレットを抽出
        if len(palettes) > max_items:
            palettes = random.sample(palettes, max_items)

        # パレットを表示する際の正方形のサイズと間隔
        square_size = 1
        num_rows = (len(palettes) + items_per_row - 1) // items_per_row  # パレットの行数を計算

        # パレットを横に並べて表示
        ax.axis('off')
        ax.set_title(f"Color Scheme: {pattern}", fontsize=14)

        for i, hex_palette in enumerate(palettes):
            # パレット内の色をSaturationでソート
            sorted_palette = sort_palette_by_saturation(hex_palette)

            row = i // items_per_row
            col = i % items_per_row

            # パレット内の4つの色（gapなし）
            for j, hex_color in enumerate(sorted_palette):
                # 正方形を描画 (パレット同士は palette_gap 間隔)
                rect = mpatches.Rectangle(
                    ((col * (4 * square_size + palette_gap)) + j * square_size, -row * (square_size + palette_gap)),
                    # xとy位置を調整
                    square_size,  # 正方形の幅
                    square_size,  # 正方形の高さ
                    facecolor=hex_color.hex_value
                )
                ax.add_patch(rect)

        # x軸とy軸の範囲を調整
        ax.set_xlim(0, items_per_row * (4 * square_size + palette_gap))
        ax.set_ylim(-num_rows * (square_size + palette_gap), square_size + palette_gap)

    plt.tight_layout()
    plt.show()


def group_by_color_scheme(results):
    """配色パターンごとに結果をグループ化する関数"""
    grouped_palettes = defaultdict(list)

    for result in results:
        final_pattern = result["final_pattern"]
        hex_palette = result["hex_palette"]
        grouped_palettes[final_pattern].append(hex_palette)

    return grouped_palettes


if __name__ == "__main__":
    # 判定結果データのパス
    results_path = '../../data/results/palette_results.json'  # 更新されたファイルパス
    results = load_results(results_path)

    # 配色パターンごとにグループ化
    grouped_palettes = group_by_color_scheme(results)

    # パレット全体をHueでソート
    sort_palettes_by_hue(grouped_palettes)

    # グループ化されたカラーパレットをまとめて表示
    plot_grouped_palettes(grouped_palettes, "Grouped Color Schemes", max_items=300, palette_gap=0.5, items_per_row=20)
