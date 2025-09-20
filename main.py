import sys, os , argparse, subprocess

from toolset.settings import CreateDefaults, OverrideColors, LoadSettings, LoadColors
from toolset.utils import CoalesseColorsToHex
from toolset.quantize import Quantizer
from toolset.vectorize import Vectorizer

class Args:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Process an image with optional parameters.")
        self._add_arguments()
        self.args = self.parser.parse_args()

    def _add_arguments(self):
        self.parser.add_argument('-p', '--palette', type=str, help='Color palette string in hex (separated by commas)')
        self.parser.add_argument('-o', '--output', type=str, help='Output file path')
        self.parser.add_argument('-i', '--input', type=str, help='Input file path')
        self.parser.add_argument('--Image', action='store_true', help='Flag for only image quantization')
        self.parser.add_argument('--AddPalette' , action='store_true', help='Put pallete on image, usually used with --Image')
    def get(self):
        return self.args

def main():
    print("Hello from imagetoprintable!")
    args = Args().get()
    #print(args)

    #! setup
    CreateDefaults()

    palettechoice = args.palette if args.palette else ""
    chex = CoalesseColorsToHex(palettechoice.split(","))
    #print(chex)

    if len(chex) > 0: OverrideColors(chex)

    settings = LoadSettings()
    if not settings: 
        print("Failed to load settings. Exiting.")
        return

    #! operations
    quantizer = Quantizer(settings["colors"])
    quantized_image_path = quantizer.quantize_image(image_path=args.input, output_path=args.output)

    if args.AddPalette and quantized_image_path:
        quantizer.color_palette_on_image(image_path=quantized_image_path, output_path=quantized_image_path)

    if args.Image:
        cleanup()
        return

    # now do the svg conversion on the output of quatization
    print("VECTOR")
    v = Vectorizer()
    v.create_bitmaps(quantized_image_path, settings["colors"])

    cleanup()


def cleanup():
    try: os.remove("settings.json")
    except: pass #print("Failed to remove settings.json")
    try: os.remove(".working.json")
    except: pass #print("Failed to remove .working.json")

if __name__ == "__main__":
    main()
