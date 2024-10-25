import numpy as np
import matplotlib.pyplot as plt
from skimage.color import rgb2lab, lab2lch

# Constants
POINT_SIZE = 60
FIGURE_SIZE = (24, 6)

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

# Generate RGB colors with equal intervals
n_intervals = 20
r_values = np.linspace(0, 1, n_intervals)
g_values = np.linspace(0, 1, n_intervals)
b_values = np.linspace(0, 1, n_intervals)
rgb_colors = np.array([[r, g, b] for r in r_values for g in g_values for b in b_values])

# Convert RGB colors to sRGB
srgb_colors = np.array([[(c * 255).astype(int) / 255 for c in color] for color in rgb_colors])

# Convert sRGB to OKLAB
oklab_colors = np.array([rgb_to_oklab(color) for color in srgb_colors])

# Convert OKLAB to OKLCH
oklch_colors = np.array([lab2lch(oklab.reshape(1, 1, 3)).reshape(3) for oklab in oklab_colors])

# Plotting in 3D space
fig = plt.figure(figsize=FIGURE_SIZE)

# RGB Plot
ax1 = fig.add_subplot(141, projection='3d')
ax1.scatter(rgb_colors[:, 0], rgb_colors[:, 1], rgb_colors[:, 2], c=rgb_colors, s=POINT_SIZE)
ax1.set_title('RGB Color Space')
ax1.set_xlabel('R')
ax1.set_ylabel('G')
ax1.set_ylim(1, 0)
ax1.set_zlabel('B')

# sRGB Plot
ax2 = fig.add_subplot(142, projection='3d')
ax2.scatter(srgb_colors[:, 0], srgb_colors[:, 1], srgb_colors[:, 2], c=rgb_colors, s=POINT_SIZE)
ax2.set_title('sRGB Color Space')
ax2.set_xlabel('R')
ax2.set_ylabel('G')
ax2.set_ylim(1, 0)
ax2.set_zlabel('B')

# OKLAB Plot
ax3 = fig.add_subplot(143, projection='3d')
ax3.scatter(oklab_colors[:, 1], oklab_colors[:, 2], oklab_colors[:, 0], c=rgb_colors, s=POINT_SIZE)
ax3.set_title('OKLAB Color Space')
ax3.set_xlabel('a')
ax3.set_ylabel('b')
ax3.set_zlabel('L')

# OKLCH Plot
ax4 = fig.add_subplot(144, projection='3d')
ax4.scatter(oklch_colors[:, 2], oklch_colors[:, 0], oklch_colors[:, 1], c=rgb_colors, s=POINT_SIZE)
ax4.set_title('OKLCH Color Space')
ax4.set_xlabel('H')
ax4.set_ylabel('L')
ax4.set_ylim(100, 0)
ax4.set_zlabel('C')

plt.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.1, wspace=0.3)
plt.show()
