
def RGBtoHex(rgb:list) -> str:
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])

def GenerateGrayscalePaletteString(steps:int=8) -> str:
    if steps < 2: steps = 2
    if steps > 256: steps = 256
    step_size = 255 // (steps - 1)
    colors = []
    for i in range(steps):
        gray_value = i * step_size
        colors.append(RGBtoHex([gray_value, gray_value, gray_value]))
    return ','.join(colors)

def CoalesseColorsToHex(color_list:list[str]) -> list:
    #! assuming the list is any color format separated by commas
    l = []
    for c in color_list:
        c = c.strip()
        if c.startswith("#"):
            #! hex format
            if len(c) != 7:
                print("Invalid hex color:", c)
                continue
            try:
                int(c[1:], 16)
            except ValueError:
                
                continue
        else:
            #! rgb format
            parts = c.split()
            if len(parts) != 3:
                print("Invalid RGB color:", c)
                continue
            try:
                r, g, b = map(lambda x: int(float(x) * 255) if 0.0 <= float(x) <= 1.0 else int(float(x)), parts)
                if not all(0 <= val <= 255 for val in (r, g, b)):
                    continue
                c = RGBtoHex([r, g, b])
            except ValueError:
                print("Invalid RGB color:", c)
                continue
        
        l.append(c.upper())

    return l