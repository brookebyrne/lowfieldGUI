import sys
import re
import numpy as np
from lowfieldGUI.pytnt_2025.pytnt.processTNT import TNTfile
import matplotlib.pyplot as plt

def read_amplitude_table(file_path, table_name):
    if len(sys.argv) != 3:
        print("Usage: python script.py <file_path> <amplitude_table_name>")
        sys.exit(1)

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            data = f.read()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        sys.exit(1)

    # Build dynamic regex using the table name
    pattern = fr'{re.escape(table_name)}(.*?)\x02'

    # multiple instances of the table name in the file
    halfway = len(data) // 2
    data = data[halfway:]

    match = re.search(pattern, data, re.DOTALL)
    if match:
        middle_section = match.group(1)

        # Match numbers with optional decimals
        number_matches = re.findall(r'\d+(?:\.\d+)?', middle_section)

        # Convert all to float
        all_numbers = [float(n) for n in number_matches]

        # Drop the first and last numbers if they're unwanted junk
        if len(all_numbers) > 2:
            cleaned_numbers = all_numbers[1:-1]
        else:
            cleaned_numbers = all_numbers

        # Convert to NumPy array
        numbers = np.array(cleaned_numbers)
        return numbers

    else:
        print(f"No section found for table: {table_name} in file: {file_path}. Check the table name and try again.")


tnt_file_name = sys.argv[1]
amplitude_table_name = sys.argv[2]

tnt = TNTfile(tnt_file_name)

fid_data = tnt.DATA
#   The first dimension represents the number of data points in the FID.
#   The second dimension represents the number of scanner amplitudes tested
fid_data.dtype
type('complex64')

scanner_amp_vals = read_amplitude_table(tnt_file_name, amplitude_table_name)
print(scanner_amp_vals)

signal_amp_vals = np.zeros(len(scanner_amp_vals))

for i in range(len(scanner_amp_vals)):
    signal = np.abs(fid_data[:, i, 0, 0]) # This takes the absolute value of the signal
    max_val = np.max(signal)
    signal_amp_vals[i] = max_val

ind = np.argmax(signal_amp_vals)
best_scanner_amp = scanner_amp_vals[ind]
print(f"Best scanner amplitude: {best_scanner_amp}")

plt.plot(scanner_amp_vals, signal_amp_vals)
plt.xlabel('Scanner Amplitude')
plt.ylabel('MaximumSignal Amplitude')
plt.title('Flip Angle Calibration Plot')
plt.show()


