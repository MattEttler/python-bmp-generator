from .create_bmp import create_bmp
import argparse

def main():
    parser = argparse.ArgumentParser(description='Generate bitmap images.', prog='python-bmp-generator OR python3 -m python-bmp-generator',)
    parser.add_argument('-o', '--output', type=str, default='output.bmp', required=False, metavar='',
            help='the name that will be given to the output file (default: output.bmp)')
    parser.add_argument('-W', '--width', type=int, default=100, choices=range(1,4001), required=False, metavar='',
            help='the pixel-width of the image that will be generated within the range 1..4000. (default: 100)')
    parser.add_argument('-H', '--height', type=int, default=100, choices=range(1,4001), required=False, metavar='',
            help='the pixel-height of the image that will be generated within the range 1..4000. (default: 100)')
    parser.add_argument('-r', '--red', type=int, default=255, choices=range(0,256), required=False, metavar='',
            help='the red-value of the image that will be generated within the range 0..255. (default: 255)')
    parser.add_argument('-g', '--green', type=int, default=0, choices=range(0,256), required=False, metavar='',
            help='the green-value of the image that will be generated within the rage 0..255. (default: 0)')
    parser.add_argument('-b', '--blue', type=int, default=255, choices=range(0,256), required=False, metavar='',
            help='the blue-value of the image that will be generated within the range 0..255. (default: 255)')

    args = parser.parse_args()
    create_bmp(file_name=args.output, width=args.width, height=args.height, red=args.red, green=args.green, blue=args.blue)
