import filecmp
from pathlib import Path
import pytest

from kingcon_python.converter import to_bitplanes, to_mask_bitplane, save_bpl, save_raw_palette
from kingcon_python.loader import load_image_and_palette

def test_to_bitplanes_exact_word():
    """Tests conversion of a 16x1 image (exactly one 16-bit word)."""
    pixels = bytes([
        1, 0, 1, 0, 0, 0, 0, 0,  # 10100000 = 0xA0
        1, 1, 1, 1, 0, 0, 0, 1   # 11110001 = 0xF1
    ])
    
    bpl = to_bitplanes(pixels, width=16, height=1, num_planes=1)
    
    assert len(bpl) == 2
    assert bpl[0] == 0xA0
    assert bpl[1] == 0xF1

def test_to_bitplanes_word_padding():
    """Tests that a 3-pixel wide image is padded to a full 16-bit word (2 bytes)."""
    pixels = bytes([1, 0, 1]) # 10100000 = 0xA0, followed by padding
    bpl = to_bitplanes(pixels, width=3, height=1, num_planes=1)
    
    assert len(bpl) == 2
    assert bpl[0] == 0xA0
    assert bpl[1] == 0x00

def test_to_bitplanes_multi_plane():
    """Tests conversion with multiple bitplanes."""
    # Pixels: 3 (binary 11), 2 (binary 10), 1 (binary 01), 0 (binary 00)
    pixels = bytes([3, 2, 1, 0])
    bpl = to_bitplanes(pixels, width=4, height=1, num_planes=2)
    
    # Plane 0 (LSB): 1, 0, 1, 0 -> 10100000 -> 0xA0
    # Plane 1 (MSB): 1, 1, 0, 0 -> 11000000 -> 0xC0
    # With word padding, each plane is 2 bytes (16 bits)
    assert len(bpl) == 4
    assert bpl[0] == 0xA0  # Plane 0, byte 0
    assert bpl[1] == 0x00  # Plane 0, byte 1 (padding)
    assert bpl[2] == 0xC0  # Plane 1, byte 0
    assert bpl[3] == 0x00  # Plane 1, byte 1 (padding)

def test_to_mask_bitplane():
    """Tests mask generation where index 0 is 0 and anything else is 1."""
    pixels = bytes([0, 5, 0, 255])
    # Expected bits: 0, 1, 0, 1 -> 01010000 -> 0x50
    mask = to_mask_bitplane(pixels, width=4, height=1)
    
    assert len(mask) == 2
    assert mask[0] == 0x50
    assert mask[1] == 0x00

TEST_DIR = Path(__file__).parent
INPUT_DIR = TEST_DIR / "input"
EXPECTED_DIR = TEST_DIR / "expected"
OUTPUT_DIR = TEST_DIR / "output"

def get_input_files():
    """Retrieve all PNG files dynamically from the tests/input directory."""
    if not INPUT_DIR.exists():
        return []
    return list(INPUT_DIR.glob("*.png"))

@pytest.mark.parametrize("img_path", get_input_files(), ids=lambda p: p.name)
def test_integration_conversion(img_path: Path):
    """End-to-End integration test comparing output files to expected C++ files."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    file_stem = img_path.stem
    # In kingcon, masks use format=1, standard files use format=5.
    is_mask = "_mask" in file_stem.lower()
    num_planes = 1 if is_mask else 5
    max_colors = 1 << num_planes
    
    # 1. Run the core loader and conversion process
    img, palette = load_image_and_palette(str(img_path), max_colors)
    bpl_out = OUTPUT_DIR / f"{file_stem}.bpl"
    save_bpl(str(bpl_out), img, num_planes)
    
    # 2. Compare BPL (Amiga formats often use upper or lowercase extensions)
    expected_bpl = EXPECTED_DIR / f"{file_stem}.BPL"
    if not expected_bpl.exists():
        expected_bpl = EXPECTED_DIR / f"{file_stem}.bpl"
    
    assert expected_bpl.exists(), f"Expected BPL missing: {expected_bpl}"
    assert filecmp.cmp(bpl_out, expected_bpl, shallow=False), f"BPL mismatch for {file_stem}"
    
    # 3. Compare PAL if it exists in the expected directory
    expected_pal = EXPECTED_DIR / f"{file_stem}.PAL"
    if not expected_pal.exists():
        expected_pal = EXPECTED_DIR / f"{file_stem}.pal"
        
    if expected_pal.exists():
        pal_out = OUTPUT_DIR / f"{file_stem}.pal"
        save_raw_palette(str(pal_out), palette)
        assert filecmp.cmp(pal_out, expected_pal, shallow=False), f"PAL mismatch for {file_stem}"
