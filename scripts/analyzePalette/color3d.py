import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from skimage.color import rgb2lab, lab2lch
from IPython.display import HTML

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

# Function to flatten color analyzePalette and convert to different color spaces
def process_color_palette(rgb_colors):
    # Convert RGB to Linear RGB and then to OKLAB
    oklab_colors = np.array([rgb_to_oklab(color) for color in rgb_colors])
    # Convert OKLAB to OKLCH
    oklch_colors = np.array([oklab_to_oklch(oklab) for oklab in oklab_colors])
    return rgb_colors, oklab_colors, oklch_colors

# Plotting function for 4 color spaces
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

# Function to add animation to sRGB color space plot
def plot_srgb_color_space_with_animation(rgb_colors, point_size=POINT_SIZE):
    fig = plt.figure(figsize=FIGURE_SIZE)
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(rgb_colors[:, 0], rgb_colors[:, 1], rgb_colors[:, 2], c=rgb_colors, s=point_size)
    ax.set_title('sRGB Color Space')
    ax.set_xlabel('R')
    ax.set_xlim(0, 1)
    ax.set_ylabel('G')
    ax.set_ylim(1, 0)
    ax.set_zlabel('B')
    ax.set_zlim(0, 1)

    def update(frame):
        angle = frame
        ax.view_init(elev=20, azim=angle)
        return ax,

    ani = animation.FuncAnimation(fig, update, frames=np.arange(0, 360, 18), interval=50, blit=False)
    plt.close(fig)
    return HTML(ani.to_jshtml())

# Function to add animation to OKLAB color space plot
def plot_oklab_color_space_with_animation(oklab_colors, rgb_colors, point_size=POINT_SIZE):
    fig = plt.figure(figsize=FIGURE_SIZE)
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(oklab_colors[:, 1], oklab_colors[:, 2], oklab_colors[:, 0], c=rgb_colors, s=point_size)
    ax.set_title('OKLAB Color Space')
    ax.set_xlabel('a')
    ax.set_ylabel('b')
    ax.set_ylim(-100, 100)
    ax.set_zlabel('L')
    ax.set_zlim(0, 100)

    def update(frame):
        angle = frame
        ax.view_init(elev=20, azim=angle)
        return ax,

    ani = animation.FuncAnimation(fig, update, frames=np.arange(0, 360, 18), interval=50, blit=False)
    plt.close(fig)
    return HTML(ani.to_jshtml())

# Function to add animation to OKLCH color space plot
def plot_oklch_color_space_with_animation(oklch_colors, rgb_colors, point_size=POINT_SIZE):
    fig = plt.figure(figsize=FIGURE_SIZE)
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(oklch_colors[:, 2], oklch_colors[:, 0], oklch_colors[:, 1], c=rgb_colors, s=point_size)
    ax.set_title('OKLCH Color Space')
    ax.set_xlabel('H')
    ax.set_ylabel('L')
    ax.set_ylim(100, 0)
    ax.set_zlabel('C')
    ax.set_zlim(0, 120)

    def update(frame):
        angle = frame
        ax.view_init(elev=20, azim=angle)
        return ax,

    ani = animation.FuncAnimation(fig, update, frames=np.arange(0, 360, 18), interval=50, blit=False)
    plt.close(fig)
    return HTML(ani.to_jshtml())

# Plotting function for H segments in LC plane (2D)
def plot_oklch_segments(oklch_colors, rgb_colors, point_size=POINT_SIZE, fig_size=(24,12)):
    # Divide H into 12 segments (0 to 2π)
    h_segments = np.linspace(0, 2 * np.pi, 13)

    fig, axes = plt.subplots(2, 6, figsize=fig_size)
    axes = axes.flatten()

    for i in range(12):
        h_min = h_segments[i]
        h_max = h_segments[i + 1]

        # Filter colors in the current H segment
        mask = (oklch_colors[:, 2] >= h_min) & (oklch_colors[:, 2] < h_max)
        filtered_colors = oklch_colors[mask]
        rgb_filtered_colors = rgb_colors[mask]
        num_points = len(filtered_colors)

        # Plot L vs C for the current H segment
        ax = axes[i]
        ax.scatter(filtered_colors[:, 0], filtered_colors[:, 1], c=rgb_filtered_colors, s=point_size)
        ax.set_title(f'H: {np.degrees(h_min):.1f}° - {np.degrees(h_max):.1f}° / Points: {num_points}')
        ax.set_xlabel('Lightness (L)')
        ax.set_ylabel('Chroma (C)')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 140)

    plt.tight_layout()
    plt.show()
