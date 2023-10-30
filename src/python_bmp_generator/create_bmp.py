import logging
import struct

from python_bmp_generator import bmp_header
from python_bmp_generator import bmp_info_header


def create_bmp(
        file_name="output.bmp",
        width=10,
        height=10,
        red=255,
        green=0,
        blue=255
):
    """
    Create a black bitmap file with a bit-depth of 24.

    Keyword arguments:
    file_name -- the name of the bitmap file that will be written (default 'output.bmp')
    width -- the desired width in pixels of the bitmap file that will be \
        created (default 10)
    height -- the desired height in pixels of the bitmap file that will be \
        created (default 10)
    red -- the intensity value of red which can be set between 0 - 255
    green -- the intensity value of green which can be set between 0 - 255
    blue -- the intensity value of blue which can be set between 0 - 255
    """

    logging.info(f"Opening {file_name} for writing.")
    with open(file_name, "wb") as file:
        file_bytearray = bytearray()

        # Create File Header Template
        logging.debug(f"the header is {bmp_header.HEADER_SIZE} bytes large.")
        file_bytearray.extend(bmp_header.HEADER_SIZE*bmp_header.ZERO)

        # Create BITMAPINFOHEADER Template
        logging.debug("creating placeholder elements for BMPINFOHEADER")
        file_bytearray.extend(
            bmp_info_header.BMP_INFO_HEADER_SIZE*bmp_header.ZERO
        )

        # Create Pixel Array
        BITS_IN_BYTE = 8
        COLOR_DEPTH = 24
        byte_alignment_size = 4
        bytes_per_pixel = (COLOR_DEPTH // BITS_IN_BYTE)
        pixel_bytes_per_row = (bytes_per_pixel * width)
        padding_bytes_per_row = (byte_alignment_size - pixel_bytes_per_row) \
            % byte_alignment_size
        pixel_array = bytearray(
            (([blue, green, red]*width) + ([0]*padding_bytes_per_row))
            * height)

        logging.debug(f"bytes_per_pixel: {bytes_per_pixel}")
        logging.debug(f"pixel array created with {len(pixel_array)} bytes {padding_bytes_per_row*height} of which are padding.")

        # hydrate the BITMAPINFOHEADER with the width in pixels
        packed_width = struct.pack('<i', width)
        file_bytearray[bmp_info_header.PIXELS_WIDTH_OFFSET:bmp_info_header.PIXELS_WIDTH_OFFSET +
                       bmp_info_header.PIXELS_WIDTH_BYTES] = packed_width

        # hydrate the BITMAPINFOHEADER with the height in pixels
        packed_height = struct.pack('<i', height)
        file_bytearray[bmp_info_header.PIXELS_HEIGHT_OFFSET:bmp_info_header.PIXELS_HEIGHT_OFFSET +
                       bmp_info_header.PIXELS_HEIGHT_BYTES] = packed_height

        # hydrate the ID/Header Field 'BM'.
        file_bytearray[:bmp_header.HEADER_FIELD_BYTES] = bmp_header.HEADER_FIELD_VALUE

        # hydrate the size of the BITMAPINFOHEADER after it has been hydrated with all other information.
        logging.debug(
            f"BITMAPINFOHEADER is {bmp_info_header.BMP_INFO_HEADER_SIZE} bytes.")
        packed_bmp_info_header = struct.pack(
            '<i', bmp_info_header.BMP_INFO_HEADER_SIZE)
        file_bytearray[bmp_info_header.HEADER_SIZE_OFFSET:bmp_info_header.HEADER_SIZE_OFFSET +
                       bmp_info_header.HEADER_SIZE_BYTES] = packed_bmp_info_header

        # hydrate the header with the number of color planes (must be 1 according to wikipedia)
        logging.debug("setting the number of color planes to 1")
        packed_number_of_planes = struct.pack('<h', 1)
        file_bytearray[bmp_info_header.NUMBER_OF_COLOR_PLANES_OFFSET:bmp_info_header.NUMBER_OF_COLOR_PLANES_OFFSET +
                       bmp_info_header.NUMBER_OF_COLOR_PLANES_BYTES] = packed_number_of_planes

        # hydrate the color bit-depth.
        logging.debug(f"setting the color depth to {COLOR_DEPTH}")
        packed_bit_depth = struct.pack('<h', COLOR_DEPTH)
        file_bytearray[bmp_info_header.PIXEL_DEPTH_OFFSET:bmp_info_header.PIXEL_DEPTH_OFFSET +
                       bmp_info_header.PIXEL_DEPTH_BYTES] = packed_bit_depth

        # hydrate the header with the offset of the pixel array (after the header data)
        logging.debug(f"pixel Array Offset is at {len(file_bytearray)}.")
        packed_pixels_address = struct.pack('<i', len(file_bytearray))
        file_bytearray[bmp_header.PIXEL_ARRAY_STARTING_ADDRESS_OFFSET:bmp_header.PIXEL_ARRAY_STARTING_ADDRESS_OFFSET +
                       bmp_header.PIXEL_ARRAY_STARTING_ADDRESS_BYTES] = packed_pixels_address

        file_bytearray.extend(pixel_array)

        # Lastly, hydrate the header with the size of the entire file
        logging.debug(f"total file size: {len(file_bytearray)} bytes")
        packed_file_size = struct.pack('<i', len(file_bytearray))
        file_bytearray[bmp_header.SIZE_OFFSET:bmp_header.SIZE_OFFSET +
                       bmp_header.SIZE_BYTES] = packed_file_size

        file.write(file_bytearray)
        logging.info(f"finished writing {file_name}")
        logging.debug(file_bytearray)


def main():
    logging.basicConfig(level=logging.INFO)
    create_bmp()


if __name__ == '__main__':
    main()
