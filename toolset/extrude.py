import os 
import trimesh
import numpy as np
from PIL import Image
from toolset.quantize import rgb_to_lab


class Extruder:
    def __init__(self, bitmaps_folder=None, svg_folder=None, layer_height_mm=10 , instructions_file="instructions.md"):
        self.bitmaps_folder = bitmaps_folder
        self.svg_folder = svg_folder
        self.layer_height_mm = layer_height_mm
        self.instructions = instructions_file
    
    def start_instructions(self):
        with open(self.instructions , 't+w') as f:
            f.writelines([
                "# Guide" , "This will tell you what heights to put the filament stops", "## Layers"
            ])

    # will create a stl for for each layer/bitmap file 
    def extrude_with_bitmap(self):
        bitmap_files = [f for f in os.listdir(self.bitmaps_folder) if f.endswith('.png')]
        rgb_colors = [tuple(f.replace('.png','').split('_')[1:]) for f in bitmap_files]
        color_to_file = dict(zip(rgb_colors , bitmap_files))

        lab_to_rgb = {tuple(rgb_to_lab([int(c) for c in rgb])): rgb for rgb in rgb_colors}
        lab_colors = sorted(lab_to_rgb.keys(), key=lambda x: x[0] , reverse=True) # sort by L value
        def make_voxel(x, y, z=0, size=1.0):
            cube = trimesh.creation.box(extents=(size, size, size))
            cube.apply_translation((x + size / 2, y + size / 2, z + size / 2))
            return cube
        #* REFACTORING
        # start from the top (lightest color)
        # for each pixel/voxel placed recored that in a seperate 'placed' array
        # this will be used to place voxels under the layer above it
        #! need to convert all of this to use the trimesh builtin voxel grid system

        for i, c in enumerate(lab_colors):
            rgb_color = lab_to_rgb[c]
            img_path = os.path.join(self.bitmaps_folder, color_to_file[rgb_color])
            img = Image.open(img_path).convert("RGBA")
            data = np.array(img)  # Shape: (height, width, 4)
            height, width = data.shape[:2]
            voxels = []
            # read in the bitmap and extrude it based on 'i'
            # create a cube shape for that pixel from y= 0 to y = i * layer_height_mm
            # for now it will lazily make each voxel/cube, no optimization or quad merging

            for y in range(height):
                for x in range(width):
                    r, g, b, a = data[y, x]
                    if (r, g, b) == (0, 0, 0) and a > 0:
                        voxel = make_voxel(x, y, z=0)  # Flip Y
                        voxels.append(voxel)

            if voxels:
                mesh = trimesh.util.concatenate(voxels)
                mesh.export(f"{color_to_file[rgb_color]}.stl")
                print(f"Exported: {color_to_file[rgb_color]}.stl")
                with open(self.instructions , "a") as f:
                    f.writelines(
                        [f"At Layer {i}" , f"swap to the filament closest to {rgb_color}" , f"At height {i*self.layer_height_mm}"]
                    )
        
    