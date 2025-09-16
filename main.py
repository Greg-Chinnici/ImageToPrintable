import sys, os , argparse

from toolset.settings import CreateDefaults, OverrideColors, LoadSettings
from toolset.utils import RGBtoHex, CoalesseColors
from toolset.quantize import quantize_image

def main():
    print("Hello from imagetoprintable!")
    #! setup
    #! assuming the cli will pass in any color format separated by commas
    CreateDefaults()

    inputstring = "#FF00ff,0 255 0 , 0 0 0 , 255 255 255 , #ffaabb , #abcabc"
    coalhex = CoalesseColors(inputstring.split(","))
    print(coalhex)

    OverrideColors(coalhex)

    settings = LoadSettings()
    if not settings: 
        print("Failed to load settings. Exiting.")
        return

    #! operations
    quantize_image("input.png", 2)


if __name__ == "__main__":
    main()
