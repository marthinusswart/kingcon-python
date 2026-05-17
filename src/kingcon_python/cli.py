import argparse
import sys
from .loader import load_image_and_palette
from .converter import save_bpl, save_raw_palette, save_tga_preview, save_mask

def main():
    parser = argparse.ArgumentParser(description="Kingcon - PNG to Amiga format converter")
    parser.add_argument("input", help="Input PNG file")
    parser.add_argument("output", help="Output file prefix")
    
    # Argparse supports `-Format=5` natively as long as we define it correctly.
    parser.add_argument("-Format", type=int, default=5, help="Number of bitplanes (e.g., 5)")
    parser.add_argument("-RawPalette", action="store_true", help="Export raw palette (.pal)")
    parser.add_argument("-Mask", action="store_true", help="Extract and save a mask bitplane")
    
    args = parser.parse_args()
    
    try:
        # Calculate the maximum number of colors based on the requested bitplanes
        # Example: 5 bitplanes = 2^5 = 32 colors
        max_colors = 1 << args.Format
        img, palette = load_image_and_palette(args.input, max_colors)
        
        # 1. Save BPL
        bpl_path = f"{args.output}.bpl"
        save_bpl(bpl_path, img, args.Format)
        print(f"Generated Bitplanes: {bpl_path}")
        
        # 2. Save Palette if requested
        if args.RawPalette:
            pal_path = f"{args.output}.pal"
            save_raw_palette(pal_path, palette)
            print(f"Generated Raw Palette: {pal_path}")
            
        # 3. Save TGA preview
        tga_path = f"{args.output}.tga"
        save_tga_preview(tga_path, img)
        print(f"Generated TGA Preview: {tga_path}")
        
        # 4. Save Mask if requested
        if args.Mask:
            mask_path = f"{args.output}_mask.bpl"
            save_mask(mask_path, img)
            print(f"Generated Mask: {mask_path}")
        
    except Exception as e:
        print(f"Error converting {args.input}: {e}", file=sys.stderr)
        sys.exit(1)