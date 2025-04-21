# calibrate the scanner amplitude to the maximum signal amplitude
# run a series of FID at different scanner amplitudes
# find the scanner amplitude that gives the maximum signal amplitude

import sys
import re
import numpy as np
from lowfieldGUI.pytnt_2025.pytnt.processTNT import TNTfile
import matplotlib.pyplot as plt

def readAmpTbl(table_name, file_path):
    """
    reads the scanner amplitudes from the tnt file

    table_name is the name of the table that contains the scanner amplitudes
    table_name is set when running the scan in Tecmag"
    """ 
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
        sys.exit(1)

# Read tnt file
if len(sys.argv) < 2:
    print("Usage: python calAmp.py <table_name> <file_path>")
    sys.exit(1)

table_name = sys.argv[1]
file_path = sys.argv[2]

# find the scanner amplitude that gives the strongest signal.
tnt = TNTfile(file_path)

fid_data = tnt.DATA
fid_data.dtype
type('complex64')

scanner_amplitudes = readAmpTbl(table_name, file_path)
signal_peaks = np.zeros(len(scanner_amplitudes))
signal_peaks.dtype = np.complex64 # initializing 

for i in range(len(scanner_amplitudes)):
    signal_peaks[i] = np.max(fid_data[:, i, 0, 0])

#find where the signal peaks and continues downwards
for i in range(1, len(signal_peaks)-1):  # Start from 1 to avoid boundary issues
    if signal_peaks[i-1] < signal_peaks[i] > signal_peaks[i+1]:  # Local maxima check
        best_scanner_amp = scanner_amplitudes[i]
        ind = i
        break  # Exit the loop once a local maxima is founds
    else:
        ind = np.argmax(signal_peaks)
        best_scanner_amp = scanner_amplitudes[ind]

print(f"Best scanner amplitude: {best_scanner_amp}")
plt.plot(scanner_amplitudes, np.real(signal_peaks))
plt.xlabel('Scanner Amplitude')
plt.ylabel('Maximum Signal Amplitude')
plt.scatter(best_scanner_amp, np.real(signal_peaks[ind]), color='red', label='Best Scanner Amplitude',zorder=5)
plt.title('Signal Amplitude vs Scanner Amplitude')
plt.show()

