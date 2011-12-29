#!/usr/bin/env python

from glob import glob
import Image
import itertools
from math import ceil, sqrt
from os.path import basename, splitext
import sys

def usage(name, message = None):
    print("Usage: {0} h[orizontal] | v[ertical] | g[rid] FILE-1 [... FILE-n] OUTFILE".format(name))
    print("  horizontal: Place images side-by-side")
    print("  vertical:   Stack images on top of each other")
    print("  grid:       Align images into a grid")
    if message is not None:
        println(" -> {0}".format(message))
    sys.exit(1)

def parseargs(args):
    if len(args) < 4:
        usage(args[0])
    formats = ('horizontal', 'vertical', 'grid')
    format_ = args[1]
    if format_ not in formats and format_ not in [f[0] for f in formats]:
        usage(args[0])
    return format_[0], list(itertools.chain.from_iterable([glob(arg) for arg in args[2:-1]])), args[-1]

def main(args):
    format_, filenames, outfilename = parseargs(args)
    mode = None
    width, height = 0, 0
    modes = []
    sizes = []
    # Store sizes and modes of all input images
    for filename in filenames:
        image = Image.open(filename)
        modes.append(image.mode)
        sizes.append(image.size)
    # Determine mode that will minimize information loss
    #   If all images have the same mode, we use that one.
    #   Otherwise, we choose a mode that best encompasses all modes,
    #   knownmodes precedence is left-to-right
    uniquemodes = set(modes)
    knownmodes = ['CYMK', 'RGBA', 'YCbCr', 'RGB', 'P', 'I', 'F', 'L', '1']
    if len(uniquemodes) == 1:
        mode = uniquemodes.pop()
    else:
        for knownmode in knownmodes:
            if knownmode in uniquemodes:
                mode = knownmode
                break
        if mode is None:
            raise Error("Couldn't choose optimal mode from {0}".format(', '.join(mode)))
    # Determine how big each "cell" in the joined image is, as well as its final dimensions
    delta_x = max([x for x, y in sizes])
    delta_y = max([y for x, y in sizes])
    if format_ == 'h':
        # Horizontal
        width, height = delta_x * len(sizes), delta_y
        delta_y = 0
    elif format_ == 'v':
        # Vertical
        width, height = delta_x, delta_y * len(sizes)
        delta_x = 0
    elif format_ == 'g':
        # Grid
        width, height = delta_x * int(ceil(sqrt(len(sizes)))), delta_y * int(round(sqrt(len(sizes))))
    outbasename = splitext(basename(outfilename))[0]
    # Display CSS template for sprites
    print(".{0} {{ display: block; width: {1}px; height: {2}px; background: url({3}) 0 0 no-repeat; overflow: hidden; }}".format(outbasename, delta_x, delta_y, outfilename))
    x, y = 0, 0
    outimage = Image.new(mode, (width, height))
    for index, filename in enumerate(filenames):
        image = Image.open(filename)
        outimage.paste(image, (x, y))
        # Display CSS offset for individual sprite
        print(".{0}.{1} {{ background-position: {2}{3}{4} {5}{6}{7}; }}".format(outbasename, splitext(basename(filename))[0], '-' if x > 0 else '', x, 'px' if x > 0 else '', '-' if y > 0 else '', y, 'px' if y > 0 else ''))
        if format_ == 'g':
            # Move to next column
            x += delta_x
            if x + 1 > width:
                # Move to next row and first column
                x = 0
                y += delta_y
        else:
            # Move to next column/row
            x += delta_x
            y += delta_y
    outimage.save(outfilename)

if __name__ == '__main__':
    main(sys.argv)
