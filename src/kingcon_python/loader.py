from PIL import Image
from typing import Tuple, List

def load_image_and_palette(filepath: str, max_colors: int) -> Tuple[Image.Image, List[int]]:
    """
    Loads an image, ensures it is palletized to the required depth,
    and extracts the 12-bit Amiga palette (0x0RGB).
    """
    img = Image.open(filepath)
    
    # Ensure the image is palletized ('P' mode) and restricted to our color depth
    if img.mode != 'P':
        img = img.convert('RGB').quantize(colors=max_colors)
        
    palette_bytes = img.getpalette()
    amiga_palette = []
    
    if palette_bytes:
        # getpalette returns a flat list: [r, g, b, r, g, b, ...]
        for i in range(0, min(len(palette_bytes), max_colors * 3), 3):
            r = palette_bytes[i]
            g = palette_bytes[i+1]
            b = palette_bytes[i+2]
            
            # Convert standard RGB to Amiga 12-bit (4 bits per channel)
            amiga_color = ((r >> 4) << 8) | ((g >> 4) << 4) | (b >> 4)
            amiga_palette.append(amiga_color)
    
    # Replicate the FreeImage artifact for 100% binary compatibility with C++ kingcon.
    # FreeImage expands palettes to 8-bit using a grayscale ramp where R=i, G=i, B=i.
    while len(amiga_palette) < max_colors:
        i = len(amiga_palette)
        quirk_color = ((i >> 4) << 8) | ((i >> 4) << 4) | (i >> 4)
        amiga_palette.append(quirk_color)
        
    return img, amiga_palette