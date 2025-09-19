import sys, os , argparse

from toolset.settings import CreateDefaults, OverrideColors, LoadSettings, LoadColors
from toolset.utils import CoalesseColorsToHex
from toolset.quantize import Quantizer

def main():
    print("Hello from imagetoprintable!")
    #! setup
    CreateDefaults()

    inputstring = "#000000 , #FFFFFF, #e88504 , #888888" # from argparse eventually
    inputstring = ''
    chex = CoalesseColorsToHex(inputstring.split(","))
    print(chex)

    if len(chex) > 0: OverrideColors(chex)

    settings = LoadSettings()
    if not settings: 
        print("Failed to load settings. Exiting.")
        return

    #! operations
    q = Quantizer(settings["colors"])
    q.quantize_image(image_path="test.png")


    #! cleanup
    try: os.remove("settings.json")
    except: print("Failed to remove settings.json")
    try: os.remove(".working.json")
    except: print("Failed to remove .working.json")

if __name__ == "__main__":
    main()
