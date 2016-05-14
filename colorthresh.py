import argparse
from PIL import Image, ImageEnhance


class Filter():
    def __init__(self):
        pass

    def filter(self, image, **kwargs):
        pixel = image.load()

        for i in range(image.size[0]):
            for j in range(image.size[1]):
                a, b, c = pixel[i, j]
                pixel[i, j] = self.modify(a, b, c, **kwargs)

        return image

    def modify(self, a, b, c, **kwargs):
        return a, b, c


class HSVThreshold(object, Filter):
    def filter(self, image, **kwargs):
        return super(HSVThreshold, self).filter(image.convert("HSV"), **kwargs)

    def modify(self, a, b, c, **kwargs):
        if c > kwargs["threshold"]:
            return 0, 0, 255
        else:
            return a, 255, c


class RGBThreshold(object, Filter):
    def filter(self, image, **kwargs):
        return super(RGBThreshold, self).filter(image.convert("RGB"), **kwargs)

    def modify(self, a, b, c, **kwargs):
        t = kwargs["threshold"]

        # Red
        if a < t:
            a = 0

        # Green
        if b < t:
            b = 0

        # Blue
        if c < t:
            c = 0

        return self.select_max(a, b, c)

    @staticmethod
    def select_max(a, b, c):
        if a > 0 and b > 0 and c > 0: return 255, 255, 255
        if a > 0 and a >= b and a >= c: return 255, 0, 0
        if b > 0 and b >= a and b >= c: return 0, 255, 0
        if c > 0 and c >= a and c >= b: return 0, 0, 255
        return 0, 0, 0


'''
Argument parsing is handled at this point
'''
parser = argparse.ArgumentParser()
parser.add_argument('input', type=str, help='Input file')
parser.add_argument('--output', type=str, default='-', help='Output file')
parser.add_argument('--threshold', type=int, choices=range(0, 255), default=180)
parser.add_argument('--colormodel', type=str, choices=['hsv', 'rgb'], default='rgb', help="The color-model to use")
parser.add_argument('--contrast', type=float, default=1.0)
parser.add_argument('--sharpness', type=float, default=1.0)
parser.add_argument('--brightness', type=float, default=1.0)
parser.add_argument('--color', type=float, default=1.0)

args = parser.parse_args()

# Read the image
im = Image.open(args.input)
im = ImageEnhance.Contrast(image=im).enhance(args.color)
im = ImageEnhance.Brightness(image=im).enhance(args.brightness)
im = ImageEnhance.Sharpness(image=im).enhance(args.sharpness)
im = ImageEnhance.Contrast(image=im).enhance(args.contrast)

if args.colormodel == 'rgb':
    im = RGBThreshold().filter(im, threshold=args.threshold)
elif args.colormodel == 'hsv':
    im = HSVThreshold().filter(im, threshold=args.threshold)

if args.output == '-':
    im.show()
else:
    im.convert("RGB").save(args.output)
