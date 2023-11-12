import logging

def convert_rgb_to_yCbCr(pixel_array):
    """ 
    Convert an array of RGB pixels (every three tuples represents one pixel in reverse-order i.e. b, g, r)
    into YCbCr colorspace.

    Keyword arguments:
    rgb_pixel_array -- where each value is a whole number between 0 and 255 representing the color instensity.
    """

    for i in range(0, len(pixel_array), 3):
        # values per-pixel are loaded in reverse so no conversion needs to happen when creating BMP
        b, g, r = pixel_array[i:i+3]
        # convert Red to Y
        pixel_array[i+2] =  max(-128, min(127, int(0.2990 * r + 0.5870 * g + 0.1140 * b - 128)))
        # convert Green to Cb
        pixel_array[i+1] = max(-128, min(127, int(-0.1687 * r - 0.3313 * g + 0.5000 * b)))
        # convert Bue to Cr
        pixel_array[i] =  max(-128, min(127, int(0.5000 *  r - 0.4187 * g - 0.0813 * b)))

    logging.debug(f"YCbCr data: {pixel_array}")
    return pixel_array
