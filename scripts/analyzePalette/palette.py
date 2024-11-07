import json
import scripts.common.color as color
import numpy as np
import itertools as itertools

# 色相の距離を計算する関数
def calculate_hue_distance(hue1, hue2):
    """2つの色相間の距離を計算する"""
    diff = abs(hue1 - hue2)
    return min(diff, 360 - diff)


# 各配色手法のスコアリング関数
def score_monochromatic(hsl_palette):
    """モノクロマティック配色のスコアを計算する"""
    hues = [hsl.h for hsl in hsl_palette]
    max_diff = max(calculate_hue_distance(hues[i], hues[j]) for i in range(len(hues)) for j in range(i + 1, len(hues)))
    if max_diff <= 5:  # 5度以内ならモノクロマティック
        return 5
    return 0


def score_analogous(hsl_palette):
    """アナロゴス配色のスコアを計算する"""
    hues = [hsl.h for hsl in hsl_palette]
    max_diff = max(calculate_hue_distance(hues[i], hues[j]) for i in range(len(hues)) for j in range(i + 1, len(hues)))
    if max_diff <= 30:  # 30度以内ならアナロゴス
        return 5
    elif max_diff <= 60:
        return 3
    return 0


def score_complementary(hsl_palette):
    """補色配色のスコアを計算する"""
    hues = [hsl.h for hsl in hsl_palette]
    if any(calculate_hue_distance(hues[i], hues[j]) in range(175, 185) for i in range(len(hues)) for j in
           range(i + 1, len(hues))):
        return 5
    return 0


def score_split_complementary(hsl_palette):
    """スプリット補色配色のスコアを計算する"""
    hues = [hsl.h for hsl in hsl_palette]
    for i in range(len(hues)):
        for j in range(i + 1, len(hues)):
            diff = calculate_hue_distance(hues[i], hues[j])
            if 150 <= diff <= 180:
                return 5
    return 0


def score_triad(hsl_palette):
    """トライアド配色のスコアを計算する"""
    hues = [hsl.h for hsl in hsl_palette]
    for i in range(len(hues)):
        for j in range(i + 1, len(hues)):
            diff = calculate_hue_distance(hues[i], hues[j])
            if 115 <= diff <= 125:
                return 5
    return 0


def score_tetrad(hsl_palette):
    """テトラード配色のスコアを計算する"""
    hues = [hsl.h for hsl in hsl_palette]
    for i in range(len(hues)):
        for j in range(i + 1, len(hues)):
            diff = calculate_hue_distance(hues[i], hues[j])
            if 85 <= diff <= 95:
                return 5
    return 0


def score_oklch_balance(oklch_palette):
    """OKLCHに基づく視覚的調和のスコアを計算する"""
    distances = [np.linalg.norm([oklch_palette[i].L - oklch_palette[j].L,
                                 oklch_palette[i].C - oklch_palette[j].C,
                                 oklch_palette[i].H - oklch_palette[j].H])
                 for i in range(len(oklch_palette)) for j in range(i + 1, len(oklch_palette))]
    avg_distance = sum(distances) / len(distances)
    if avg_distance < 0.2:  # 小さいほど調和が取れている
        return 5
    return 0


# 総合スコアを計算する関数
def calculate_total_score(srgb_palette):
    # sRGBをHSL、OKLCHに変換
    hsl_palette = [hex_color.to_hsl() for hex_color in srgb_palette]
    oklch_palette = [hex_color.to_oklch() for hex_color in srgb_palette]

    scores = {
        "monochromatic": score_monochromatic(hsl_palette),
        "analogous": score_analogous(hsl_palette),
        "complementary": score_complementary(hsl_palette),
        "split_complementary": score_split_complementary(hsl_palette),
        "triad": score_triad(hsl_palette),
        "tetrad": score_tetrad(hsl_palette),
        "oklch_balance": score_oklch_balance(oklch_palette)
    }

    # 最もスコアが高い配色手法を選択
    best_match = max(scores, key=scores.get)

    return best_match, scores


# 3色ずつの組み合わせで判定
def determine_color_scheme_for_4_colors(hex_palette: list[str]) -> tuple[str, list]:
    # 3色の組み合わせを抽出
    color_combinations = list(itertools.combinations(hex_palette, 3))
    combination_scores = []

    # 各3色の組み合わせに対して配色手法を判定
    for combination in color_combinations:
        rgb_palette = [color.Hex(hex_color).to_srgb() for hex_color in combination]
        best_match, scores = calculate_total_score(rgb_palette)
        combination_scores.append((combination, best_match, scores))

    # 結果を統合して最終的な配色パターンを決定
    pattern_counts = {}
    for _, best_match, _ in combination_scores:
        if best_match in pattern_counts:
            pattern_counts[best_match] += 1
        else:
            pattern_counts[best_match] = 1

    # 最も多く出現したパターンを最終的な配色パターンとして決定
    final_pattern = max(pattern_counts, key=pattern_counts.get)

    return final_pattern, combination_scores

def process_color_data(data: list[list[str]]) -> list[str]:
    """
    カラーパレットデータを処理し、各パレットに対して配色パターンを判定する。

    Parameters:
    data (np.array): OKLCH色空間で表されたカラーパレットデータ

    Returns:
    results (list): 各パレットに対して判定された配色パターンとその詳細
    """
    results: list[dict] = []

    for hex_palette in data:
        # 配色パターンの判定
        final_pattern, combination_scores = determine_color_scheme_for_4_colors(hex_palette)

        # 結果を保存
        result: dict = {
            "hex_palette": [hex_color for hex_color in hex_palette],
            "final_pattern": final_pattern,
            "combination_scores": combination_scores
        }
        results.append(result)

    return results


def save_results(results, output_path):
    """
    判定結果をJSONファイルとして保存する関数。

    Parameters:
    results (list): 判定された結果のリスト
    output_path (str): 結果を保存するファイルのパス
    """
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=4)


def load_data(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return np.array(data)  # NumPy配列に変換


if __name__ == "__main__":
    # データの読み込み
    data_path = '../../data/raw/rgbPalette.json'  # 訓練データのファイルパス
    data: list[list[str]] = load_data(data_path)

    # カラーパレットデータを処理し、配色パターンを判定
    results = process_color_data(data)

    # 結果の保存
    output_path = '../../data/results/palette_results.json'
    save_results(results, output_path)

    print(f"結果が {output_path} に保存されました。")