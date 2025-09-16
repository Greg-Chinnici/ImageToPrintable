
def RGBtoHex(rgb:list) -> str:
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])

def CoalesseColors(color_list:list[str]) -> list:
    #! assuming the cli will pass in any color format separated by commas
    l = []
    for c in color_list:
        c = c.strip()
        if c.startswith("#"):
            #! hex format
            if len(c) != 7:
                continue
            try:
                int(c[1:], 16)
            except ValueError:
                continue
        else:
            #! rgb format
            parts = c.split()
            if len(parts) != 3:
                continue
            try:
                r, g, b = map(int, parts)
                if not all(0 <= val <= 255 for val in (r, g, b)):
                    continue
                c = RGBtoHex([r, g, b])
            except ValueError:
                continue
        
        l.append(c.upper())

    return l