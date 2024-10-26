import numpy as np
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

class RGB:
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

def srgb_to_oklab(c: RGB) -> OKLab:
    """
    sRGBからOKLab色空間に変換する関数。

    Parameters:
    c (RGB): 変換するRGBオブジェクト

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

def srgb_to_oklch(c: RGB) -> OKLCH:
    """
    sRGBからOKLCH色空間に変換する関数。

    Parameters:
    c (RGB): 変換するRGBオブジェクト

    Returns:
    OKLCH: 変換されたOKLCHオブジェクト
    """
    oklab = srgb_to_oklab(c)
    return oklab_to_oklch(oklab)

def oklch_to_srgb(c: OKLCH) -> RGB:
    """
    OKLCH色空間からsRGBに変換する関数。

    Parameters:
    c (OKLCH): 変換するOKLCHオブジェクト

    Returns:
    RGB: 変換されたRGBオブジェクト
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

def oklab_to_srgb(c: OKLab) -> RGB:
    """
    OKLab色空間からsRGBに変換する関数。

    Parameters:
    c (OKLab): 変換するOKLabオブジェクト

    Returns:
    RGB: 変換されたRGBオブジェクト
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

    return RGB(*rgb)
