import os
import numpy as np
from ReadData import read_raw_field
from ReadData import read_tecmag_channels

def read_tecmag(filename, dsize, *args):
    try:
        # If no filename is provided, prompt the user to select a file
        if not filename:
            filename = os.path.normpath(input("Enter the file path: "))

        header = read_tecmag_hdr(filename)
        data_size = header['acq_points']
        actual_npts = header['actual_npts']

        if len(args) < 3:
            if len(args) < 2:
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
            data = read_raw_field(filename, offset, [2] + dsize, 'float', 'l')
            data = data[0, :, :, :, :] + 1j * data[1, :, :, :, :]
            data = np.squeeze(data)

        else:
            num_points = actual_npts[1]
            channels = read_tecmag_channels(filename, header['data_bytes'])
            num_channels = len(channels)

            if num_channels == 1:
                print(f'Acquisition detected on channel {channels}')
            else:
                print(f'Acquisition detected on channels {", ".join(map(str, channels))}')

            if len(args) < 2:
                sorted_flag = False
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
            data = read_raw_field(filename, offset, dsize, 'float', 'l', *args)

            num_sa1 = len([ch for ch in channels if ch <= 4])
            num_sa2 = len([ch for ch in channels if ch >= 5])

            if sorted_flag:
                data = np.reshape(data, (data_size[0], num_points, num_channels))
                data = np.transpose(data, [0, 2, 1])
            else:
                data2 = np.zeros((num_channels, data_size[0], num_points))
                for loop in range(num_points):
                    data2[0:num_sa1, :, loop] = np.reshape(data[loop * num_channels * data_size[0]:(loop * num_channels * data_size[0]) + num_sa1 * data_size[0]], (num_sa1, data_size[0], 1))
                    data2[num_sa1:num_channels, :, loop] = np.reshape(data[(loop * num_channels * data_size[0]) + num_sa1 * data_size[0]:(loop + 1) * num_channels * data_size[0]], (num_sa2, data_size[0], 1))
                data = np.transpose(data2, [1, 2, 0])

        return data, header, var_data

    except Exception as e:
        print(f"Error: {e}")
        return None, None, None

def read_tecmag_hdr(filename):
    try:
        header = {}
        with open(filename, 'rb') as file_pt:
            header['acq_points'] = tuple(np.fromfile(file_pt, dtype=np.int32, count=2))
            header['actual_npts'] = tuple(np.fromfile(file_pt, dtype=np.int32, count=4))
            header['data_bytes'] = np.fromfile(file_pt, dtype=np.int32, count=1)[0]
        return header
    except Exception as e:
        print(f"Error: {e}")
        return None
