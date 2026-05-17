# Kingcon Migration Guide: C++ to Python

This document outlines the architectural strategy for migrating `kingcon`, a PNG to Amiga-style format (BPL, SPR, etc.) converter, from C++ to Python.

## 1. Data Structure Mapping

In Python, we should favor `dataclasses` for internal configuration and the `struct` module for handling binary layouts and big-endian conversions.

### Config and State (Internal)
The `Image` and `Data` structs should be converted to `dataclasses`.

| C++ Struct | Python Equivalent | Purpose |
| :--- | :--- | :--- |
| `Image` | `dataclass` (e.g., `ImageConfig`) | Stores conversion settings (format, bitplanes, mode). |
| `Cutout` | `dataclass` (e.g., `Cutout`) | Tracks x, y, width, height, and pixel data for a specific cutout. |
| `Bob` | `struct` format string `'>HHHHLL'` | The binary structure saved to disk. |
| `LineColorEntry` | `int` or `tuple` | Represents a 12-bit Amiga color (0xRGB). |

### Binary Structures (Disk Output)
Amiga is a **Big Endian** system. Python's `struct` module is perfect for this.

```python
import struct
from dataclasses import dataclass

@dataclass
class Bob:
    width_in_words: int
    height: int
    width: int
    offset: int
    anchor_x: int
    anchor_y: int

    def pack(self):
        # Amiga/Big-Endian format: >
        # H: unsigned short (2 bytes), L: unsigned long (4 bytes)
        # Note: anchor_x/y are signed short 'h' in C++ but often stored as unsigned
        return struct.pack('>HHHLhh', 
            self.width_in_words, 
            self.height, 
            self.width, 
            self.offset, 
            self.anchor_x, 
            self.anchor_y
        )
```

## 2. Recommended Python Libraries

| C++ Dependency | Python Replacement | Reasoning |
| :--- | :--- | :--- |
| `FreeImage` | `Pillow` (PIL) | Industry standard for image loading, palletization, and manipulation. |
| `stdlib.h` (Memory) | `bytearray` / `bytes` | Safe, native buffer handling. |
| `arpa/inet.h` (Endianness) | `struct` module | Explicit control over byte order (Big Endian `>`). |
| Custom `CFormatSaver` | Abstract Base Class (ABC) | Clean polymorphic design for different output formats. |

## 3. Core Conversion Algorithm Breakdown

The migration should follow a modular pipeline:

### Step 1: Image Loading & Preprocessing
Use `Pillow` to load the image.
- **Palletization**: Use `image.quantize(colors=N)` to reduce the palette.
- **Masking**: Extract the alpha channel using `image.split()[-1]` or identify the "transparent" color index.
- **12-bit Conversion**: Amiga colors are typically 4 bits per channel (0xRGB). 
  - Python: `(r >> 4) << 8 | (g >> 4) << 4 | (b >> 4)`

### Step 2: Cutout Extraction
For `IM_Bob` or `IM_Font` modes:
- Iterate through the image pixels to find bounding boxes.
- Create `Cutout` objects containing the sub-images.

### Step 3: Format Specific Conversion (The "Saver" Logic)

#### Bitplane (BPL) Conversion
To convert a chunky palletized image to bitplanes:
1. For each scanline:
2. For each bitplane `p` from `0` to `numBitplanes - 1`:
3. For each pixel in the scanline:
4. If `(pixel_index >> p) & 1`, set the corresponding bit in the bitplane buffer.

```python
def to_bitplanes(pixels, width, height, num_planes):
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
```

### Step 4: Binary Output
- Combine the header (e.g., `BOB` list) and the raw data.
- Ensure all multi-byte values are packed with `struct.pack('>...')`.

## 4. Potential Edge Cases & Endianness

- **Endianness**: **Crucial.** Always use the `>` prefix in `struct.pack`. Amiga hardware expects big-endian words and longs.
- **Word Alignment**: Amiga Bitplanes must be word-aligned (16 bits). Padding bytes must be added if the image width is not a multiple of 16.
- **Interleaving**: Some Amiga formats expect bitplanes to be interleaved (Scanline 0 Plane 0, Scanline 0 Plane 1, etc.) rather than planar (All Scanlines Plane 0, All Scanlines Plane 1). The Python implementation should support both via a toggle.
- **12-bit vs 24-bit Palettes**: 
  - OCS/ECS (12-bit): 2 bytes per color (`0000RRRRGGGGBBBB`).
  - AGA (24-bit): 4 bytes per color (typically `00RRRRRRRRGGGGGGGGBBBBBBBB`).
- **FreeImage vs Pillow Coordinates**: FreeImage can be bottom-to-top. `kingcon.cpp` explicitly flips vertically. Pillow is top-to-bottom, so this flip might be unnecessary in the Python version, but check against the original output to be sure.
