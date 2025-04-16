# calibrate the scanner amplitude to the maximum signal amplitude
# run a series of FID at different scanner amplitudes
# find the scanner amplitude that gives the maximum signal amplitude

import sys
import re
import numpy as np
from lowfieldGUI.pytnt_2025.pytnt.processTNT import TNTfile
import matplotlib.pyplot as plt

def readAmpTbl(table_name, file_path):

    # opening the tnt file as utf-8 text file
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            data = f.read()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        sys.exit(1)

    # Build dynamic regex using the table name
    # pattern = fr'{re.escape(table_name)}(.*?)\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x003R'

    pattern = fr'\x00\x00\x00{re.escape(table_name)}(.*?)3R'

    # multiple instances of the table name in the file in earlier sections irrelevant to the task, 
    # trying to skip to the end of the file where the the information we care about is
    halfway = len(data) // 2
    data = data[halfway:]

    match = re.search(pattern, data, re.DOTALL)
    if match:
        middle_section = match.group(1)

        # Match numbers with optional decimals
        number_matches = re.findall(r'(?<![\d])\d+(?:\.\d+)?(?![\d])', middle_section)

        # Convert all to float
        numbers = [float(n) for n in number_matches]
        if numbers[0] == 0:
                numbers = numbers[1:]
        elif numbers[1] == 0:
                numbers = numbers[2:]

        # Convert to NumPy array
        scanner_amplitudes = np.array(numbers)
        return scanner_amplitudes
        
    else:
        print(f"No section found for table: {table_name} in file: {file_path}. Check the table name and try again.")


def calAmp(table_name, file_path):
    # find the scanner amplitude that gives the maximum signal amplitude and most power

    tnt = TNTfile(file_path)

    fid_data = tnt.DATA
    fid_data.dtype
    type('complex64')

    scanner_amplitudes = readAmpTbl(table_name, file_path)
    signal_peaks = np.zeros(len(scanner_amplitudes)) # initializing 
    fig, axs = plt.subplots(len(scanner_amplitudes))

    for i in range(len(scanner_amplitudes)):
        signal = np.abs(fid_data[:15, i, 0, 0]) # This takes the absolute value of the signal
        signal_peaks[i] = np.max(signal)
        axs[i].plot(signal)
        axs[i].set_title(f'received signal at each scanner amplitude')
    
        
    plt.show()
    ind = np.argmax(signal_peaks)
    best_scanner_amp = scanner_amplitudes[ind]
    return best_scanner_amp, signal_peaks, scanner_amplitudes


# Read tnt file
if len(sys.argv) < 2:
    print("Usage: python calAmp.py <able_name> <file_path>")
    sys.exit(1)

table_name = sys.argv[1]
file_path = sys.argv[2]

best_scanner_amp, signal_peaks, scanner_amplitudes = calAmp(table_name, file_path)

# uncomment to see outputs

print(f"Best scanner amplitude: {best_scanner_amp}")
plt.plot(scanner_amplitudes, signal_peaks)
plt.xlabel('Scanner Amplitude')
plt.ylabel('Maximum Signal Amplitude')
plt.title('Signal Amplitude vs Scanner Amplitude')
plt.show()
# # plt.savefig(file_path + '.png')


