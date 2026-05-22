import argparse
import sys
import os
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
        
        generated_files = []
        
        # 1. Save BPL
        bpl_path = f"{args.output}.bpl"
        save_bpl(bpl_path, img, args.Format)
        generated_files.append(("Bitplanes", bpl_path))
        
        # 2. Save Palette if requested
        if args.RawPalette:
            pal_path = f"{args.output}.pal"
            save_raw_palette(pal_path, palette)
            generated_files.append(("Raw Palette", pal_path))
            
        # 3. Save TGA preview
        tga_path = f"{args.output}.tga"
        save_tga_preview(tga_path, img)
        generated_files.append(("TGA Preview", tga_path))
        
        # 4. Save Mask if requested
        if args.Mask:
            mask_path = f"{args.output}_mask.bpl"
            save_mask(mask_path, img)
            generated_files.append(("Mask", mask_path))
            
        # Terminal formatting for summary table
        C_CYAN = "\033[96m"
        C_GREEN = "\033[92m"
        C_YELLOW = "\033[93m"
        C_MAGENTA = "\033[95m"
        C_BOLD = "\033[1m"
        C_RESET = "\033[0m"

        width, height = img.size
        val_input = os.path.basename(args.input)
        val_dims = f"{width}x{height}"
        val_planes = f"{args.Format} planes ({max_colors} colors)"
        
        left_width = 18
        right_width = max(len(val_input), len(val_dims), len(val_planes))
        for _, path in generated_files:
            right_width = max(right_width, len(path))
        right_width = max(right_width + 2, 25)

        def print_row(label, value, color):
            print(f"{C_MAGENTA}│{C_RESET} {C_YELLOW}{label:<{left_width}}{C_RESET} {C_MAGENTA}│{C_RESET} {color}{value:<{right_width}}{C_RESET} {C_MAGENTA}│{C_RESET}")

        print(f"\n{C_MAGENTA}┌{'─' * (left_width + right_width + 5)}┐{C_RESET}")
        print(f"{C_MAGENTA}│{C_RESET} {C_CYAN}{C_BOLD}{'Bitplane Conversion Summary':<{left_width + right_width + 3}}{C_RESET} {C_MAGENTA}│{C_RESET}")
        print(f"{C_MAGENTA}├{'─' * (left_width + 2)}┬{'─' * (right_width + 2)}┤{C_RESET}")
        print_row("Input image", val_input, C_GREEN)
        print_row("Dimensions", val_dims, C_GREEN)
        print_row("Format", val_planes, C_GREEN)
        print(f"{C_MAGENTA}├{'─' * (left_width + 2)}┼{'─' * (right_width + 2)}┤{C_RESET}")
        
        for label, path in generated_files:
            print_row(label, path, C_CYAN)
            
        print(f"{C_MAGENTA}└{'─' * (left_width + 2)}┴{'─' * (right_width + 2)}┘{C_RESET}")
        
    except Exception as e:
        print(f"Error converting {args.input}: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
