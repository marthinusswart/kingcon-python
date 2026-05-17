import struct
from dataclasses import dataclass
from typing import List

@dataclass
class Cutout:
    """Tracks bounds and pixel data for a specific image cutout."""
    x: int
    y: int
    width: int
    height: int
    pixels: List[int]

@dataclass
class Bob:
    """Represents the binary header structure for a Bob saved to disk."""
    width_in_words: int
    height: int
    width: int
    offset: int
    anchor_x: int
    anchor_y: int

    def pack(self) -> bytes:
        """
        Packs the Bob structure into Amiga Big-Endian format.
        Format string '>HHHLhh' breakdown:
        > : Big-endian
        H : unsigned short (2 bytes), L : unsigned long (4 bytes), h : signed short (2 bytes)
        """
        return struct.pack(
            '>HHHLhh', 
            self.width_in_words, 
            self.height, 
            self.width, 
            self.offset, 
            self.anchor_x, 
            self.anchor_y
        )