#!/usr/bin/env python3
import os
import argparse

from GBCameraPlugin import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dump Game Boy Camera pictures from a save file")
    parser.add_argument("file", type=str, help="Input file")
    parser.add_argument("out_dir", type=str, help="Output directory")
    parser.add_argument("--format", type=str, default="png", help="Output format (defaults to png)")
    parser.add_argument("--pal", type=str, default="classic", choices=PALETTES.keys(), help="Palette to use")
    args = parser.parse_args()

    try:
        os.mkdir(args.out_dir)
    except FileExistsError:
        pass
    except:
        print("Error creating directory:", args.out_dir)
        exit(1)

    try:
        img = Image.open(args.file)
    except:
        print("Error opening file:", args.file)
        exit(1)

    img.putpalette(PALETTES[args.pal])
    for i in range(30):
        img.seek(i)
        img.save("{}/{:02d}.{}".format(args.out_dir, i, args.format))

    img.close()
    print("Success!")
