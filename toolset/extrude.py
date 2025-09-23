import os 
from PIL import Image
from quantize import rgb_to_lab


class Extruder:
    def __init__(self, bitmaps_folder, svg_folder, layer_height_mm=10):
        self.bitmaps_folder = bitmaps_folder
        self.svg_folder = svg_folder
        self.layer_height_mm = layer_height_mm
        

    def extrude_with_bitmap(self):
        bitmap_files = [f for f in os.listdir(self.bitmaps_folder) if f.endswith('.png')]
        rgb_colors = [f.replace('.png','').split('_')[1:] for f in bitmap_files]
        color_to_file = dict(zip(rgb_colors , bitmap_files))

        lab_to_rgb = {tuple(rgb_to_lab([int(c) for c in rgb])): rgb for rgb in rgb_colors}
        lab_colors = sorted(lab_to_rgb.keys(), key=lambda x: x[0])

        for i, c in enumerate(lab_colors):
            rgb_color = lab_to_rgb(c)
            img_path = os.path.join(self.bitmaps_folder, color_to_file[rgb_color])
            img = Image.open(img_path)

            # read in the bitmap and extrude it based on 'i'
            # create a cube shape for that pixel from y= 0 to y = i * layer_height_mm

        pass
    