import os
import sys
import numpy as np

def read_raw_field(filename, offset, mat_size, mat_type, big_little, *args):
    try:
        # If no filename is provided, prompt the user to select a file
        if not filename:
            filename = os.path.normpath(input("Enter the file path: "))

        # If offset, mat_size, mat_type, or big_little are not provided, prompt the user for input
        if not offset or not mat_size or not mat_type or not big_little:
            offset = int(input("Enter the offset: "))
            mat_size = [int(x) for x in input("Enter the matrix dimension (e.g., [1]): ").strip("[]").split(",")]
            mat_type_list = ['schar', 'uchar', 'int8', 'int16', 'int32', 'int64', 'uint8', 'uint16', 'uint32', 'uint64', 'float32', 'float64', 'double', 'char', 'short', 'int', 'long', 'ushort', 'uint', 'ulong', 'float', 'bitN', 'ubitN']
            print("Select a type:")
            for i, t in enumerate(mat_type_list):
                print(f"{i+1}. {t}")
            mat_type_index = int(input("Enter the number corresponding to the type: "))
            mat_type = mat_type_list[mat_type_index-1]

            if mat_type in ['bitN', 'ubitN']:
                num_bits = int(input("Enter the number of bit(s): "))
                if mat_type == 'bitN':
                    mat_type = f'bit{num_bits}'
                else:
                    mat_type = f'ubit{num_bits}'

            big_little_list = ['cray', 'ieee-be', 'ieee-le', 'ieee-be.l64', 'ieee-le.l64', 'native', 'vaxd', 'vaxg']
            print("Select a Big/Little Endian:")
            for i, b in enumerate(big_little_list):
                print(f"{i+1}. {b}")
            big_little_index = int(input("Enter the number corresponding to the Big/Little Endian: "))
            big_little = big_little_list[big_little_index-1]

        # Open the file and read the data
        with open(filename, 'rb') as fp:
            fp.seek(offset, 0)
            total_size = np.prod(mat_size)
            data = np.fromfile(fp, dtype=mat_type, count=total_size)
            if len(mat_size) > 1 or mat_size[0] > 1:
                data = data.reshape(mat_size)

        return data

    except Exception as e:
        print(f"Error: {e}")
        return None