REM ..\..\tools\kingcon.exe packman_tiles.png packman_tiles -Interleaved -Format=5 -RawPalette -Mask

REM ..\..\tools\kingcon.exe pacman-Sprite-0001.png pacman-Sprite-0001 -Interleaved -Format=5 -RawPalette -Mask
REM ..\..\tools\kingcon.exe pacman-Sprite-0002_shifted_reverse.png pacman-Sprite-0002_shifted_reverse -Interleaved -Format=5 -RawPalette -Mask
REM ..\..\tools\kingcon.exe pacman-Sprite-0003_shifted.png pacman-Sprite-0003_shifted -Interleaved -Format=5 -RawPalette -Mask
REM ..\..\tools\kingcon.exe pacman-Sprite-0004.png pacman-Sprite-0004 -Interleaved -Format=5 -RawPalette -Mask

..\..\tools\kingcon.exe pacman_tiles.png pacman_tiles -Format=5 -RawPalette
..\..\tools\kingcon.exe pacman_tiles_mask.png pacman_tiles_mask -Format=1
..\..\tools\kingcon.exe stage-0001.png stage-0001 -Format=5
..\..\tools\kingcon.exe alphanumeric.png alphanumeric -Format=5
..\..\tools\kingcon.exe alphanumeric_mask.png alphanumeric_mask -Format=1

move *.bpl bpl
move *.pal bpl
move *.tga bpl
