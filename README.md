# Python Bitmap Generator

This program was created with the intent of learning how to generate bitmaps from scratch.
Please feel free to open a pull-request, issue, or fork!

This tool was built using Python version 3.11.2. I have not tested this using any other versions, although it likely works with substantially older versions of Python3.

## INSTALLATION

run `pip install python-bmp-generator`

## USAGE

### CLI

run `python-bmp-generator -h` for help.

example: `python-bmp-generator -r 0 -g 255 -b 0 -o green-image.bmp`

### Python Module

There is really only one function at this time. See "create_bmp.py" for details.

include like: `from python_bmp_generator import create_bmp`

example:
```
from python_bmp_generator import create_bmp

create_bmp(file_name="output.bmp", width=100, height=100, red=255, green=0, blue=255)
```
