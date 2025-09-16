



class Quantizer:
    def __init__(self, color_list, settings_file="settings.json"):
        self.colors = color_list
    

    def quantize_image(input_path, settings_file):
        pass
    

    def rgb_to_lab(rgb:list[int]):
        r, g, b = [c / 255 for c in rgb]

        def gamma_expand(c):
            return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
        linear = map(gamma_expand, (r, g, b))

        #D65 reference white
        X = linear[0] * 0.4124 + linear[1] * 0.3576 + linear[2] * 0.1805
        Y = linear[0] * 0.2126 + linear[1] * 0.7152 + linear[2] * 0.0722
        Z = linear[0] * 0.0193 + linear[1] * 0.1192 + linear[2] * 0.9505
    
        Xn, Yn, Zn = 95.047, 100.000, 108.883
        x = X / Xn
        y = Y / Yn
        z = Z / Zn
    
        delta = 6 / 29
        def f(t):
            return t ** (1/3) if t > delta**3 else (t / (3 * delta**2)) + (4 / 29)

        fx = f(x)
        fy = f(y)
        fz = f(z)

        L = 116 * fy - 16
        a = 500 * (fx - fy)
        b = 200 * (fy - fz)

        return [L, a, b]

