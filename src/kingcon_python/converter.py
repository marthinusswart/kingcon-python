import struct
from PIL import Image
from typing import List

def to_bitplanes(pixels: bytes, width: int, height: int, num_planes: int) -> bytearray:
    """Converts chunky pixel indices into planar Amiga bitplane data."""
    # Ensure row bytes are word-aligned (multiple of 16 bits / 2 bytes)
    row_bytes = ((width + 15) // 16) * 2
    plane_size = row_bytes * height
    buffer = bytearray(plane_size * num_planes)
    
    for y in range(height):
        for x in range(width):
            pixel = pixels[y * width + x]
            for p in range(num_planes):
                if (pixel >> p) & 1:
                    byte_idx = (p * plane_size) + (y * row_bytes) + (x // 8)
                    bit_idx = 7 - (x % 8)
                    buffer[byte_idx] |= (1 << bit_idx)
                    
    return buffer

def to_mask_bitplane(pixels: bytes, width: int, height: int) -> bytearray:
    """Converts chunky pixels into a 1-bit mask plane (1 = solid, 0 = transparent)."""
    row_bytes = ((width + 15) // 16) * 2
    plane_size = row_bytes * height
    buffer = bytearray(plane_size)
    
    for y in range(height):
        for x in range(width):
            pixel = pixels[y * width + x]
            # Index 0 is background (transparent). Any other index is solid.
            if pixel > 0:
                byte_idx = (y * row_bytes) + (x // 8)
                bit_idx = 7 - (x % 8)
                buffer[byte_idx] |= (1 << bit_idx)
                
    return buffer

def save_bpl(output_path: str, img: Image.Image, num_planes: int):
    """Extracts pixel data and saves it as an Amiga bitplane binary (.bpl)."""
    width, height = img.size
    pixels = img.tobytes()
    bpl_data = to_bitplanes(pixels, width, height, num_planes)
    with open(output_path, 'wb') as f:
        f.write(bpl_data)
        
def save_mask(output_path: str, img: Image.Image):
    """Extracts a mask from the image and saves it as a 1-bitplane binary (.bpl)."""
    width, height = img.size
    pixels = img.tobytes()
    mask_data = to_mask_bitplane(pixels, width, height)
    with open(output_path, 'wb') as f:
        f.write(mask_data)

def save_raw_palette(output_path: str, palette: List[int]):
    """Saves the 12-bit Amiga palette as Big-Endian 16-bit words (.pal)."""
    with open(output_path, 'wb') as f:
        for color in palette:
            f.write(struct.pack('>H', color))

def save_tga_preview(output_path: str, img: Image.Image):
    """Saves a TGA format preview image."""
    img.save(output_path, format="TGA")