import sys, os , argparse, subprocess

from toolset.settings import CreateDefaults, OverrideColors, LoadSettings, LoadColors
from toolset.utils import CoalesseColorsToHex
from toolset.quantize import Quantizer

class Args:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Process an image with optional parameters.")
        self._add_arguments()
        self.args = self.parser.parse_args()

    def _add_arguments(self):
        self.parser.add_argument('-p', '--palette', type=str, help='Color palette string in hex (separated by commas)')
        self.parser.add_argument('-o', '--output', type=str, help='Output file path')
        self.parser.add_argument('-i', '--input', type=str, help='Input file path')
        self.parser.add_argument('--Image', action='store_true', help='Flag for only image processing')

    def get(self):
        return self.args

def main():
    print("Hello from imagetoprintable!")
    args = Args().get()
    print(args)

    #! setup
    CreateDefaults()

    palettechoice = args.palette if args.palette else ""
    chex = CoalesseColorsToHex(palettechoice.split(","))
    print(chex)

    if len(chex) > 0: OverrideColors(chex)

    settings = LoadSettings()
    if not settings: 
        print("Failed to load settings. Exiting.")
        return

    #! operations
    quantizer = Quantizer(settings["colors"])
    quantized_image_path = quantizer.quantize_image(image_path=args.input, output_path=args.output)

    if args.Image:
        cleanup()
        return

    # now do the svg conversion on the output of quatization

    cleanup()


def cleanup():
    try: os.remove("settings.json")
    except: print("Failed to remove settings.json")
    try: os.remove(".working.json")
    except: print("Failed to remove .working.json")

if __name__ == "__main__":
    main()
