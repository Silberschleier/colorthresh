import argparse
from PIL import Image


def hsv_thresh(im, threshold = 200):
    px = im.load()

    for i in range(im.size[0]):
        for j in range(im.size[1]):
            h, s, v = px[i, j]
            if v > threshold:
                px[i, j] = (0, 0, 255)
            else:
                px[i, j] = (h, 255, v)

    return im

'''
Argument parsing is handled at this point
'''
parser = argparse.ArgumentParser()
parser.add_argument('input', type=str, help='Input file')
parser.add_argument('--output', type=str, help='Output file')
args = parser.parse_args()

# Read the image
im = Image.open(args.input).convert("HSV")

hsv_thresh(im).show()

