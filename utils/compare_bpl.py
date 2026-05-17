import sys

def compare_binaries(file1_path: str, file2_path: str, max_diffs: int = 20):
    try:
        with open(file1_path, 'rb') as f1, open(file2_path, 'rb') as f2:
            data1 = f1.read()
            data2 = f2.read()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
        
    print(f"File 1 (Python) : {file1_path} ({len(data1)} bytes)")
    print(f"File 2 (C++)    : {file2_path} ({len(data2)} bytes)")
    
    if len(data1) != len(data2):
        print("\nWARNING: File sizes do not match! Check your word-alignment logic.")
        
    diff_count = 0
    print(f"\nComparing bytes (showing up to {max_diffs} differences):")
    print(f"{'Offset':>8} | {'Py Hex':>6} | {'C++ Hex':>7} | {'Py Bin':>8} | {'C++ Bin':>8}")
    print("-" * 55)
    
    for i in range(max(len(data1), len(data2))):
        b1 = data1[i] if i < len(data1) else None
        b2 = data2[i] if i < len(data2) else None
        
        if b1 != b2:
            h1 = f"{b1:02x}" if b1 is not None else "--"
            h2 = f"{b2:02x}" if b2 is not None else "--"
            bin1 = f"{b1:08b}" if b1 is not None else "--------"
            bin2 = f"{b2:08b}" if b2 is not None else "--------"
            print(f"{i:08x} | 0x{h1} |  0x{h2} | {bin1} | {bin2}")
            diff_count += 1
            if diff_count >= max_diffs:
                break
                
    if diff_count == 0:
        print("\nSUCCESS: Files are 100% identical!")

if __name__ == '__main__':
    compare_binaries(*sys.argv[1:3] if len(sys.argv) > 2 else sys.exit("Usage: python compare_bpl.py <file1> <file2>"))