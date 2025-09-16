import sys, os , argparse

from toolset.settings import CreateDefaults, OverrideColors, LoadSettings, LoadColors
from toolset.utils import CoalesseColorsToHex
from toolset.quantize import Quantizer

def main():
    print("Hello from imagetoprintable!")
    #! setup
    CreateDefaults()

    inputstring = "#FF00ff,0 255 0 , 0 0 0 , 255 255 255 , #ffaabb , #abcabc , 0.1 0 0.2, 0.8 0.7 0.9" # from argparse eventually
    chex = CoalesseColorsToHex(inputstring.split(","))
    print(chex)

    OverrideColors(chex)

    settings = LoadSettings()
    if not settings: 
        print("Failed to load settings. Exiting.")
        return

    #! operations
    q = Quantizer(LoadColors())

    #! cleanup
    try: os.remove("settings.json")
    except: print("Failed to remove settings.json")
    try: os.remove(".working.json")
    except: print("Failed to remove .working.json")

if __name__ == "__main__":
    main()
