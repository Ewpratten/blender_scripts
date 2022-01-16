def hex_to_rgb( hex_value ):
    b = (hex_value & 0xFF) / 255.0
    g = ((hex_value >> 8) & 0xFF) / 255.0
    r = ((hex_value >> 16) & 0xFF) / 255.0
    return r, g, b