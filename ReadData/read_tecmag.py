import os
import numpy as np
from . import read_raw_field
from . import read_tecmag_header
from . import read_tecmag_hdr
import sys

def read_tecmag(filename, dsize):
    ms = []
    header = {}

    if not filename:
        filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.normpath(input("Enter the file path: ")))

    header = read_tecmag_header(filename)
    data_size = header['acq_points']
    actual_npts = header['actual_npts']

    if len(dsize) < 2:
        num_channels = actual_npts[0] // data_size[0]
        dsize = [num_channels, data_size[0]] + list(actual_npts[1:])

    header_vars = read_tecmag_hdr()

    header_name = header_vars[:, 0:28]
    header_offset = header_vars[:, 28:34]
    header_type = header_vars[:, 35:43]
    header_size = header_vars[:, 44:47]
    header_desc = header_vars[:, 47:85]

    num_vars = header_name.shape[0]

    with open(filename, 'rb') as file_pt:
        for i in range(19, 20):
            var_name = header_name[i, :].strip()
            var_offset = int(header_offset[i, :].strip())
            var_type = header_type[i, :].strip()
            var_size = int(header_size[i, :].strip())
            var_desc = header_desc[i, :].strip()

            file_pt.seek(var_offset, 0)
            var_data = np.fromfile(file_pt, dtype=var_type, count=var_size)

    offset = 1056
    ms = read_raw_field(filename, offset, [2, dsize], 'float', 'l')
    ms = ms[0, :, :, :, :] + 1j * ms[1, :, :, :, :]
    ms = np.squeeze(ms)

    return ms, header, var_data

def main():
    if len(sys.argv) != 2:
        print("Usage: python read_tecmag.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    print(f"Reading file: {filename}")

    # Call the read_tecmag function and capture the output
    dsize = []  # Define dsize as needed
    ms, header, var_data = read_tecmag(filename, dsize)

    # Print or process the output as needed
    print("Output Data:")
    print(ms)  # or any other relevant output

if __name__ == "__main__":
    main()
