import json

def CreateDefaults():
    defaults = {
        "colors": ["#FFFFFF", "#FF0000", "#00FF00", "#0000FF", "#000000"],
    }

    with open("settings.json", "w") as f:
        json.dump(defaults, f, indent=4)

def OverrideColors(colors:list[str]):
    try:
        with open("settings.json", "r+") as f:
            settings = json.load(f)
            settings["colors"] = colors
            f.seek(0)             
            json.dump(settings, f, indent=4)
            f.truncate() 
    except FileNotFoundError:
        print("Settings file not found. Using default colors.")


def LoadSettings():
    try:
        with open("settings.json", "r") as f:
            settings = json.load(f)
            return settings
    except FileNotFoundError:
        print("Settings file not found.")
        return None