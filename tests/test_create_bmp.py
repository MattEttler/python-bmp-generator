import unittest
from hypothesis import given, strategies as st, settings
import struct

from python_bmp_generator import create_bmp
from python_bmp_generator import bmp_header

class CreateBmpTestCase(unittest.TestCase):

    @given(width=st.integers(1, 14000), height=st.integers(1, 14000))
    @settings(deadline=None)
    def test_file_size_is_count_of_bytes_in_file(self, width, height):
        create_bmp(file_name="test.bmp", width=width, height=height)
        with open("test.bmp", mode='br') as file:
            file_bytearray = file.read()
            packed_file_size = struct.pack('<i', len(file_bytearray))
            actual_size = file_bytearray[bmp_header.SIZE_OFFSET:bmp_header.SIZE_OFFSET +
                    bmp_header.SIZE_BYTES]
            self.assertEqual(actual_size, packed_file_size, "the file_size header value must be set to the number of total bytes int the file.")


if __name__ == '__main__':
    unittest.main()
