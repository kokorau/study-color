import numpy as np
import matplotlib.pyplot as plt
from typing import Union

class OKLab:
    def __init__(self, L: float, a: float, b: float):
        """
        OKLab色空間を表すクラス。

        Parameters:
        L (float): 明度
        a (float): 緑-赤の成分
        b (float): 青-黄の成分
        """
        self.L = L
        self.a = a
        self.b = b

class sRGB:
    def __init__(self, r: float, g: float, b: float):
        """
        RGB色空間を表すクラス。

        Parameters:
        r (float): 赤の成分 (0.0 - 1.0)
        g (float): 緑の成分 (0.0 - 1.0)
        b (float): 青の成分 (0.0 - 1.0)
        """
        self.r = r
        self.g = g
        self.b = b

class OKLCH:
    def __init__(self, L: float, C: float, H: float):
        """
        OKLCH色空間を表すクラス。

        Parameters:
        L (float): 明度
        C (float): 彩度
        H (float): 色相 (度数法で 0 - 360)
        """
        self.L = L
        self.C = C
        self.H = H

class HSL:
    def __init__(self, h: float, s: float, l: float):
        """
        HSL色空間を表すクラス。

        Parameters:
        h (float): 色相 (0.0 - 360.0)
        s (float): 彩度 (0.0 - 1.0)
        l (float): 明度 (0.0 - 1.0)
        """
        self.h = h
        self.s = s
        self.l = l

class Hex:
    def __init__(self, hex_value: str):
        """
        Hex色を表すクラス。

        Parameters:
        hex_value (str): 16進数の色 (#rrggbb の形式)
        """
        self.hex_value = hex_value

def hex_to_srgb(hex_color: Hex) -> sRGB:
    """
    Hex色からRGB色空間に変換する関数。

    Parameters:
    hex_color (Hex): 変換するHexオブジェクト

    Returns:
    sRGB: 変換されたsRGBオブジェクト
    """
    hex_value = hex_color.hex_value.lstrip('#')
    r, g, b = tuple(int(hex_value[i:i+2], 16) / 255 for i in (0, 2, 4))
    return sRGB(r, g, b)

def srgb_to_hex(c: sRGB) -> Hex:
    """
    RGB色空間からHex色に変換する関数。

    Parameters:
    c (sRGB): 変換するsRGBオブジェクト

    Returns:
    Hex: 変換されたHexオブジェクト
    """
    hex_value = f'#{int(c.r * 255):02x}{int(c.g * 255):02x}{int(c.b * 255):02x}'
    return Hex(hex_value)

def srgb_to_hsl(c: sRGB) -> HSL:
    """
    sRGBからHSL色空間に変換する関数。

    Parameters:
    c (sRGB): 変換するsRGBオブジェクト

    Returns:
    HSL: 変換されたHSLオブジェクト
    """
    r, g, b = c.r, c.g, c.b
    max_val = max(r, g, b)
    min_val = min(r, g, b)
    l = (max_val + min_val) / 2

    if max_val == min_val:
        h = s = 0.0  # 無彩色
    else:
        d = max_val - min_val
        s = d / (1 - abs(2 * l - 1)) if l != 0 else 0

        if max_val == r:
            h = (g - b) / d + (6 if g < b else 0)
        elif max_val == g:
            h = (b - r) / d + 2
        else:
            h = (r - g) / d + 4

        h *= 60

    return HSL(h, s, l)

def hsl_to_srgb(c: HSL) -> sRGB:
    """
    HSL色空間からsRGBに変換する関数。

    Parameters:
    c (HSL): 変換するHSLオブジェクト

    Returns:
    sRGB: 変換されたsRGBオブジェクト
    """
    h, s, l = c.h, c.s, c.l
    c_val = (1 - abs(2 * l - 1)) * s
    x = c_val * (1 - abs((h / 60) % 2 - 1))
    m = l - c_val / 2

    if 0 <= h < 60:
        r, g, b = c_val, x, 0
    elif 60 <= h < 120:
        r, g, b = x, c_val, 0
    elif 120 <= h < 180:
        r, g, b = 0, c_val, x
    elif 180 <= h < 240:
        r, g, b = 0, x, c_val
    elif 240 <= h < 300:
        r, g, b = x, 0, c_val
    else:
        r, g, b = c_val, 0, x

    r = (r + m)
    g = (g + m)
    b = (b + m)

    return sRGB(r, g, b)

def srgb_to_oklab(c: sRGB) -> OKLab:
    """
    sRGBからOKLab色空間に変換する関数。

    Parameters:
    c (sRGB): 変換するsRGBオブジェクト

    Returns:
    OKLab: 変換されたOKLabオブジェクト
    """
    rgb = np.array([c.r, c.g, c.b])
    lms = np.array([
        [0.4122214708, 0.5363325363, 0.0514459929],
        [0.2119034982, 0.6806995451, 0.1073969566],
        [0.0883024619, 0.2817188376, 0.6299787005]
    ]).dot(rgb)

    lms_ = np.cbrt(np.where(lms > 0, lms, -lms)) * np.sign(lms)

    oklab = np.array([
        [0.2104542553, 0.7936177850, -0.0040720468],
        [1.9779984951, -2.4285922050, 0.4505937099],
        [0.0259040371, 0.7827717662, -0.8086757660]
    ]).dot(lms_)

    return OKLab(*oklab)

def srgb_to_oklch(c: sRGB) -> OKLCH:
    """
    sRGBからOKLCH色空間に変換する関数。

    Parameters:
    c (sRGB): 変換するsRGBオブジェクト

    Returns:
    OKLCH: 変換されたOKLCHオブジェクト
    """
    oklab = srgb_to_oklab(c)
    return oklab_to_oklch(oklab)

def oklch_to_srgb(c: OKLCH) -> sRGB:
    """
    OKLCH色空間からsRGBに変換する関数。

    Parameters:
    c (OKLCH): 変換するOKLCHオブジェクト

    Returns:
    sRGB: 変換されたsRGBオブジェクト
    """
    oklab = oklch_to_oklab(c)
    return oklab_to_srgb(oklab)

def oklab_to_oklch(c: OKLab) -> OKLCH:
    """
    OKLab色空間からOKLCH色空間に変換する関数。

    Parameters:
    c (OKLab): 変換するOKLabオブジェクト

    Returns:
    OKLCH: 変換されたOKLCHオブジェクト
    """
    L = c.L
    C = np.sqrt(c.a ** 2 + c.b ** 2)
    H = np.degrees(np.arctan2(c.b, c.a))
    if H < 0:
        H += 360
    return OKLCH(L, C, H)

def oklch_to_oklab(c: OKLCH) -> OKLab:
    """
    OKLCH色空間からOKLab色空間に変換する関数。

    Parameters:
    c (OKLCH): 変換するOKLCHオブジェクト

    Returns:
    OKLab: 変換されたOKLabオブジェクト
    """
    L = c.L
    a = c.C * np.cos(np.radians(c.H))
    b = c.C * np.sin(np.radians(c.H))
    return OKLab(L, a, b)

def oklab_to_srgb(c: OKLab) -> sRGB:
    """
    OKLab色空間からsRGBに変換する関数。

    Parameters:
    c (OKLab): 変換するOKLabオブジェクト

    Returns:
    sRGB: 変換されたsRGBオブジェクト
    """
    oklab = np.array([c.L, c.a, c.b])
    lms_ = np.array([
        [1.0, 0.3963377774, 0.2158037573],
        [1.0, -0.1055613458, -0.0638541728],
        [1.0, -0.0894841775, -1.2914855480]
    ]).dot(oklab)

    lms = lms_ ** 3

    rgb = np.array([
        [4.0767416621, -3.3077115913, 0.2309699292],
        [-1.2684380046, 2.6097574011, -0.3413193965],
        [-0.0041960863, -0.7034186147, 1.7076147010]
    ]).dot(lms)

    return sRGB(*rgb)
