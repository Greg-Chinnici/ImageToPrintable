import os 
from PIL import Image

class Extruder:
    def __init__(self, bitmaps_folder, svg_folder, layer_height_mm=10):
        pass

    def extrude_with_bitmap(self):
        bitmap_files = os.getfiles(os.path.join(self.bitmaps_folder))
        rgb_colors = [f.replace('.png','').split('_')[1:] for f in bitmap_files]
        color_to_file = dict(zip(rgb_colors , bitmap_files))
        # sort rgb to lab based on L to find height

        for i, f in enumerate(bitmap_files):
            img = Image.open(f)
            color = rgb_colors[i]
        pass
    