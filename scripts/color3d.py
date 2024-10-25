import numpy as np
import matplotlib.pyplot as plt
import json
from skimage.color import rgb2lab, lab2lch

# Constants
POINT_SIZE = 10
FIGURE_SIZE = (30, 10)

# Function to convert sRGB to Linear RGB
def srgb_to_linear(value):
    if value <= 0.04045:
        return value / 12.92
    else:
        return ((value + 0.055) / 1.055) ** 2.4

# Function to convert RGB to OKLAB (using approximation via LAB)
def rgb_to_oklab(rgb):
    # RGB to Linear RGB
    linear_rgb = np.array([srgb_to_linear(c) for c in rgb])
    return rgb2lab(linear_rgb.reshape(1, 1, 3)).reshape(3)  # Convert RGB to LAB as an approximation for OKLAB

# Function to convert OKLAB to OKLCH
def oklab_to_oklch(oklab):
    return lab2lch(oklab.reshape(1, 1, 3)).reshape(3)

# Function to flatten color palette and convert to different color spaces
def process_color_palette(palette):
    # Flatten the color palette
    flattened_palette = [color for sublist in palette for color in sublist]
    # Convert hex to RGB
    rgb_colors = np.array([[int(color[i:i+2], 16) / 255 for i in (1, 3, 5)] for color in flattened_palette])
    # Convert RGB to Linear RGB and then to OKLAB
    oklab_colors = np.array([rgb_to_oklab(color) for color in rgb_colors])
    # Convert OKLAB to OKLCH
    oklch_colors = np.array([oklab_to_oklch(oklab) for oklab in oklab_colors])
    return rgb_colors, oklab_colors, oklch_colors

# Plotting function
def plot_color_spaces(rgb_colors, oklab_colors, oklch_colors, point_size=POINT_SIZE):
    fig = plt.figure(figsize=FIGURE_SIZE)

    # sRGB Plot
    ax1 = fig.add_subplot(141, projection='3d')
    ax1.scatter(rgb_colors[:, 0], rgb_colors[:, 1], rgb_colors[:, 2], c=rgb_colors, s=point_size)
    ax1.set_title('sRGB Color Space')
    ax1.set_xlabel('R')
    ax1.set_xlim(0, 1)
    ax1.set_ylabel('G')
    ax1.set_ylim(1, 0)
    ax1.set_zlabel('B')
    ax1.set_zlim(0, 1)

    # OKLAB Plot
    ax2 = fig.add_subplot(142, projection='3d')
    ax2.scatter(oklab_colors[:, 1], oklab_colors[:, 2], oklab_colors[:, 0], c=rgb_colors, s=point_size)
    ax2.set_title('OKLAB Color Space')
    ax2.set_xlabel('a')
    ax2.set_ylabel('b')
    ax2.set_ylim(-100, 100)
    ax2.set_zlabel('L')
    ax2.set_zlim(0, 100)

    # OKLCH Plot
    ax3 = fig.add_subplot(143, projection='3d')
    ax3.scatter(oklch_colors[:, 2], oklch_colors[:, 0], oklch_colors[:, 1], c=rgb_colors, s=point_size)
    ax3.set_title('OKLCH Color Space')
    ax3.set_xlabel('H')
    ax3.set_ylabel('L')
    ax3.set_ylim(100, 0)
    ax3.set_zlabel('C')
    ax3.set_zlim(0, 120)

    plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05, wspace=0.3)
    plt.show()

# Jupyter Notebook: Function to generate color palette with equal intervals
def generate_equal_interval_palette():
    n_intervals = 10
    r_values = np.linspace(0, 1, n_intervals)
    g_values = np.linspace(0, 1, n_intervals)
    b_values = np.linspace(0, 1, n_intervals)
    rgb_colors = np.array([[r, g, b] for r in r_values for g in g_values for b in b_values])
    return rgb_colors
