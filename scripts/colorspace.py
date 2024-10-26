import convertColor
import numpy as np

def plot_oklab_color_space():
    """
    OKLab色空間の可視化を行う関数。
    sRGB空間の値を基にして、対応するOKLabの色空間を立体的にプロットします。
    """
    # sRGBの範囲内の値を設定
    r_values = np.linspace(0, 1, 20)
    g_values = np.linspace(0, 1, 20)
    b_values = np.linspace(0, 1, 20)

    r, g, b = np.meshgrid(r_values, g_values, b_values)

    # sRGBの全ての組み合わせを平坦化
    r_flat = r.flatten()
    g_flat = g.flatten()
    b_flat = b.flatten()

    # sRGBからOKLab色空間に変換
    oklab_colors = [convertColor.srgb_to_oklab(convertColor.sRGB(r, g, b)) for r, g, b in zip(r_flat, g_flat, b_flat)]
    L_flat = [c.L for c in oklab_colors]
    a_flat = [c.a for c in oklab_colors]
    b_flat = [c.b for c in oklab_colors]

    # 色空間内の色をRGBに変換してプロット用の色として使用
    colors_rgb = np.clip([[r, g, b] for r, g, b in zip(r_flat, g_flat, b_flat)], 0, 1)

    # プロットの設定
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    scatter = ax.scatter(a_flat, b_flat, L_flat, c=colors_rgb, marker='o')

    ax.set_xlabel('a')
    ax.set_ylabel('b')
    ax.set_zlabel('L')
    ax.set_title('OKLab Color Space (from sRGB)')

    plt.show()

# 例としてOKLab色空間の可視化を実行
plot_oklab_color_space()
