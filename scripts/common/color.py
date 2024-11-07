import numpy as np

class Hex:
    def __init__(self, hex_value: str):
        self.hex_value = hex_value

    def to_srgb(self):
        hex_value = self.hex_value.lstrip('#')
        r, g, b = tuple(int(hex_value[i:i + 2], 16) / 255 for i in (0, 2, 4))
        return Srgb(r, g, b)

    def to_oklab(self):
        return self.to_srgb().to_oklab()

    def to_oklch(self):
        return self.to_srgb().to_oklch()

    def to_hsl(self):
        return self.to_srgb().to_hsl()

class Srgb:
    def __init__(self, r: float, g: float, b: float):
        self.r = r
        self.g = g
        self.b = b

    def to_hex(self):
        r, g, b = self.r, self.g, self.b
        return Hex(f'#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}')

    def to_hsl(self):
        r, g, b = self.r, self.g, self.b
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

        return Hsl(h, s, l)

    def to_oklab(self):
        rgb = np.array([self.r, self.g, self.b])
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

        return Oklab(*oklab)

    def to_oklch(self):
        return self.to_oklab().to_oklch()

class Hsl:
    def __init__(self, h: float, s: float, l: float):
        self.h = h
        self.s = s
        self.l = l

    def to_srgb(self):
        h, s, l = self.h, self.s, self.l
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

        return Srgb(r + m, g + m, b + m)

    def to_hex(self):
        return self.to_srgb().to_hex()

    def to_oklab(self):
        return self.to_srgb().to_oklab()

    def to_oklch(self):
        return self.to_srgb().to_oklch()

class Oklch:
    def __init__(self, L: float, C: float, H: float):
        self.L = L
        self.C = C
        self.H = H

    def to_oklab(self):
        """OKLCHからOKLabに変換するメソッド"""
        L = self.L
        a = self.C * np.cos(np.radians(self.H))
        b = self.C * np.sin(np.radians(self.H))
        return Oklab(L, a, b)

    def to_srgb(self):
        """OKLCHからsRGBに変換するメソッド"""
        return self.to_oklab().to_srgb()

    def to_hex(self):
        """OKLCHからHex色に変換するメソッド"""
        return self.to_srgb().to_hex()

    def to_hsl(self):
        """OKLCHからHSLに変換するメソッド"""
        return self.to_srgb().to_hsl()

class Oklab:
    def __init__(self, L: float, a: float, b: float):
        self.L = L
        self.a = a
        self.b = b

    def to_oklch(self):
        L = self.L
        C = np.sqrt(self.a ** 2 + self.b ** 2)
        H = np.degrees(np.arctan2(self.b, self.a))
        if H < 0:
            H += 360
        return Oklch(L, C, H)

    def to_srgb(self):
        oklab = np.array([self.L, self.a, self.b])
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

        return Srgb(*rgb)

    def to_hex(self):
        return self.to_srgb().to_hex()

    def to_hsl(self):
        return self.to_srgb().to_hsl()
