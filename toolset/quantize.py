import numpy as np
from PIL import Image, ImageDraw
import os
from sklearn.metrics import pairwise_distances_argmin



class Quantizer:
    def __init__(self, color_list, settings_file="settings.json"):
        self.colors = color_list
        
    

    def quantize_image(self,image_path,output_path=None)->str:
        if image_path is None or not os.path.isfile(image_path):
            print("Invalid image path:", image_path)
            return None
        
        # use nearest LAB Space (need to convert target colors too)
        lab_colors: list[float] = []
        for c in self.colors:
            if not c.startswith("#") or len(c) != 7:
                print("Invalid color in settings:", c)
                continue
            rgb = self.hex_to_rgb(c)
            lab = self.rgb_to_lab(rgb)
            lab_colors.append(lab)
            #print(f"Color {c} -> RGB {rgb} -> LAB {lab}")
        

        lab_palette = np.array(lab_colors, dtype=np.float32)
        img = Image.open(image_path).convert('RGB')
        rgb_array = np.array(img, dtype=np.float32) # shape: (H, W, 3)
        rgb_flat = rgb_array.reshape(-1, 3)
        H, W = rgb_array.shape[:2]
        
        lab_pixels = [self.rgb_to_lab((r, g, b)) for r, g, b in rgb_flat]

        #! QUANTIZATION HERE, both colors are in LAB space
        indices = pairwise_distances_argmin(lab_pixels, lab_palette)  
        indices_image = indices.reshape(H, W)

        #quantized_lab_flat = lab_palette[indices]
        #quantized_lab = quantized_lab_flat.reshape(H, W, 3)

        #print(lab_palette)
        #print(rgb_array)
        #print(lab_pixels)
        #print(quantized_lab)
        #print(indices_image)
        
        output = Image.new('RGB', (W, H))
        output_pixels = output.load()
        for y in range(H):
            for x in range(W):
                color_index = indices_image[y, x]
                hex_color = self.colors[color_index]
                rgb_color = tuple(self.hex_to_rgb(hex_color))
                output_pixels[x, y] = rgb_color
        
        if output_path is None:
            output_path = os.path.splitext(image_path)[0] + "_quantized.png"

        output.save(output_path)
        print(f"Saved Quantized image to {output_path}")
        return output_path
        
    def color_palette_on_image(self,image_path,output_path=None, pallete_height_pixels=None)->str:
        if image_path is None or not os.path.isfile(image_path):
            print("Invalid image path:", image_path)
            return None
        
        img = Image.open(image_path).convert('RGB')
        W, H = img.size
        palette_height = pallete_height_pixels if pallete_height_pixels else H // 7

        if W < len(self.colors) * palette_height:
            print("Image too small for palette overlay.")
            return None
        
        new_height = H + palette_height
        output = Image.new('RGB', (W, new_height), (255, 255, 255))
        output.paste(img, (0, 0))

        colors_rgb = [tuple(self.hex_to_rgb(c)) for c in self.colors]
        color_count = len(colors_rgb)
        cell_width = W // color_count
        draw = ImageDraw.Draw(output)
        for i, color in enumerate(colors_rgb):
            x0 = i * cell_width
            x1 = x0 + cell_width

            draw.rectangle([x0, H, x1, new_height], fill=color)

        output.save(output_path)
        print(f"Saved image with palette to {output_path}")
        return output_path


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