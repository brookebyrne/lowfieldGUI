## this is a guess/try at creating this file. Need to ask charlotte for it because it is refrenced in read_tecmag
import numpy as np

def read_tecmag_channels(filename, data_bytes):
    try:
        with open(filename, 'rb') as file_pt:
            # Seek to the appropriate position in the file to read the channels
            file_pt.seek(20, 0)
            npts = tuple(np.fromfile(file_pt, dtype=np.int32, count=2))
            actual_npts = tuple(np.fromfile(file_pt, dtype=np.int32, count=4))
            data_bytes = np.fromfile(file_pt, dtype=np.int32, count=1)[0]

            # Calculate the number of channels based on the data size
            num_channels = actual_npts[0] // npts[0]

            # Read the channel information
            channels = np.arange(1, num_channels + 1)

            return channels

    except Exception as e:
        print(f"Error: {e}")
        return None