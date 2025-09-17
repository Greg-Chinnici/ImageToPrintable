

class Quantizer:
    def __init__(self, color_list, settings_file="settings.json"):
        self.colors = color_list
    

    def quantize_image(self,input_path):
        # use nearest LAB Space (need to convert target colors too)
        lab_colors = []
        for c in self.colors:
            if not c.startswith("#") or len(c) != 7:
                print("Invalid color in settings:", c)
                continue
            rgb = self.hex_to_rgb(c)
            lab = self.rgb_to_lab(rgb)
            lab_colors.append(lab)
            print(f"Color {c} -> RGB {rgb} -> LAB {lab}")
        self.colors = lab_colors
        # for each pixel in image, convert to LAB and find nearest color
        # then copy that close color into array at same pixel position
        # final image will be of same resolution but only use the colors in settings
    
    def hex_to_rgb(self, hex_color:str) -> tuple[int,int,int]:
        hex_color = hex_color.lstrip('#')
        return [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]
    
    # rgb list is 3 elements of range 0-255
    def rgb_to_lab(self, rgb: tuple[int, int, int]) -> list[float]:
        r, g, b = [c / 255.0 for c in rgb]
        
        def gamma_expand(c):
            return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
        
        linear_r, linear_g, linear_b = [gamma_expand(c) for c in (r, g, b)]
        
        # sRGB to XYZ transformation matrix (D65)
        X = linear_r * 0.4124564 + linear_g * 0.3575761 + linear_b * 0.1804375
        Y = linear_r * 0.2126729 + linear_g * 0.7151522 + linear_b * 0.0721750
        Z = linear_r * 0.0193339 + linear_g * 0.1191920 + linear_b * 0.9503041
        
        # D65 reference white
        Xn, Yn, Zn = 95.047, 100.000, 108.883
        x = X / Xn * 100  
        y = Y / Yn * 100
        z = Z / Zn * 100
        
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