# file to take output of read_tecmag.py to create an image using a fourier transform 
# make sure all the data is there, what variables do you need to run this function

import numpy as np
from scipy.fft import fft2, fftshift, ifft2
import sys
import os

def read_tecmag_hdr():
    M = {}
    M['TNT1000'] = ' 000000 '
    M['TMAG'] = ' 000008 '
    M['BOOL'] = ' 000012 '
    M['LEN'] = ' 000016 '
    M['npts'] = ' 000020 '
    M['actual_npts'] = ' 000036 '
    M['acq_points'] = ' 000052 '
    M['npts_start'] = ' 000056 '
    M['scans'] = ' 000068 '
    M['actual_scans'] = ' 000072 '
    M['dummy_scans'] = ' 000076 '
    M['repeat_times'] = ' 000080 '
    M['sadimension'] = ' 000084 '
    M['magnet_field'] = ' 000096 '
    M['ob_freq'] = ' 000104 '
    M['base_freq'] = ' 000136 '
    M['offset_freq'] = ' 000168 '
    M['ref_freq'] = ' 000200 '
    M['NMR_freq'] = ' 000208 '
    M['sw'] = ' 000260 '
    M['dwell'] = ' 000292 '
    M['filter'] = ' 000324 '
    M['experiment_time'] = ' 000332 '
    M['acq_time'] = ' 000340 '
    M['last_delay'] = ' 000348 '
    M['spectrum_direction'] = ' 000356 '
    M['hardware_sideband'] = ' 000358 '
    M['Taps'] = ' 000360 '
    M['Type'] = ' 000362 '
    M['dDigRec'] = ' 000364 '
    M['nDigitalCenter'] = ' 000368 '
    M['tramsmitter_gain'] = ' 000388 '
    M['receiver_gain'] = ' 000390 '
    M['set_spin_rate'] = ' 000408 '
    M['actual_spin_rate'] = ' 000410 '
    M['lock_field'] = ' 000412 '
    M['lock_power'] = ' 000414 '
    M['lock_gain'] = ' 000416 '
    M['lock_phase'] = ' 000418 '
    M['lock_freq_mhz'] = ' 000420 '
    M['lock_ppm'] = ' 000428 '
    M['H2O_freq_ref'] = ' 000436 '
    M['set_temperature'] = ' 000460 '
    M['actual_temperature'] = ' 000468 '
    M['shim_unit'] = ' 000476 '
    M['shims'] = ' 000484 '
    M['shims_FWHM'] = ' 000556 '
    M['HH_dcpl_attn'] = ' 000564 '
    M['DF_DN'] = ' 000566 '
    M['F1_tran_mode'] = ' 000568 '
    M['dec_BW'] = ' 000582 '
    M['grd_orientation'] = ' 000584 '
    M['date'] = ' 000884 '
    M['nucleus'] = ' 000916 '
    M['nucleus_2D'] = ' 000932 '
    M['nucleus_3D'] = ' 000948 '
    M['nucleus_4D'] = ' 000964 '
    M['sequence'] = ' 001012 '
    M['lock_solvent'] = ' 001012 '
    M['lock_nucleus'] = ' 001028 '
    print('Contents of M directory:', M)
    return M  

def read_tecmag_header(filename=None):
    header = {}
    if filename is None:
        filename = os.path.join(os.path.dirname(__file__), os.path.basename(os.path.splitext(input("Enter Tecmag NMR data file path: "))[0] + ".tnt"))
    
    if os.path.exists(filename) and os.path.getsize(filename) > 1056:
        with open(filename, 'rb') as file_pt:
            Hdr_var = read_tecmag_hdr(file_pt)
            Hdr_name = Hdr_var[:, 0:27].tolist()
            Hdr_offset = [eval(x) for x in Hdr_var[:, 27:33].tolist()]
            Hdr_type = [x.strip() for x in Hdr_var[:, 34:42].tolist()]
            Hdr_size = [eval(x) for x in Hdr_var[:, 43:46].tolist()]
            Hdr_desc = Hdr_var[:, 46:84].tolist()

            for i, (Var_name, Var_offset, Var_type, Var_size, Var_desc) in enumerate(zip(Hdr_name, Hdr_offset, Hdr_type, Hdr_size, Hdr_desc)):
                file_pt.seek(Var_offset)
                Var_data = file_pt.read(Var_size)
                if Var_type == 'char' and Var_size > 1:
                    Var_data = Var_data.decode().rstrip('\x00')
                else:
                    Var_data = Var_data
                header[Var_name.strip()] = Var_data
    print("Header contents:", header)  # Add this line to debug
    return header 

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

def read_tecmag(filename, dsize):
    ms = []
    header = {}

    if not filename:
        filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.normpath(input("Enter the file path: ")))

    header = read_tecmag_header(filename)
    print("Header contents:", header)  # Add this line to debug
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
        print("Usage: python -m ReadData.create_2D_image <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    dsize = []  # Define dsize based on your data requirements

    try:
        # Load data
        data = read_tecmag(filename, dsize)  # Pass dsize as an argument
        SE_gfruit_data = np.abs(fftshift(ifft2(data)))

        # Centering
        shifted_data = np.roll(SE_gfruit_data, [11, 5], axis=(0, 1))

        # Plot the shifted data
        import matplotlib.pyplot as plt
        plt.figure()
        plt.imshow(shifted_data, cmap='gray')
        plt.show()

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()