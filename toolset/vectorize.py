import os
from PIL import Image


class Vectorizer:
    def __init__(self, image_path , hex_colors):
        self.image_path = image_path
        self.hex_colors = hex_colors
        
        self.create_bitmaps()
    
    def create_bitmaps(self):
        img = Image.open(self.image_path).convert('RGB')
        width, height = img.size
        colors_rgb = [tuple(int((color.split('#')[1])[i:i+2], 16) for i in (0, 2, 4)) for color in self.hex_colors]
        
    
        os.makedirs("bitmaps", exist_ok=True)
        for color in colors_rgb:
            self._color_bitmap(img, color, width , height)

        
    def vectorize_image(self, image_path, output_path=None) -> str:
        if image_path is None or not os.path.isfile(image_path):
            print("Invalid image path:", image_path)
            return None
        
    
    
    def _color_bitmap(self, image , color ,width , height, preserve_color=False):
        bitmap = Image.new('RGBA', (width, height), (0, 0, 0, 0))

        pixels = image.load()
        bitmap_pixels = bitmap.load()

        for y in range(height):
            for x in range(width):
                if pixels[x, y] == color:
                    if preserve_color: bitmap_pixels[x, y] = color + (255,)
                    else: bitmap_pixels[x, y] = (0, 0, 0, 255)
        
        color_str = '_'.join(map(str, color))
        path = os.path.join('bitmaps', f'bitmap_{color_str}.png')
        bitmap.save(path)
        print(f"saving {color} bitmap at {path}")