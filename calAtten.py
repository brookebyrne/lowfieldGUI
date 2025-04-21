"""
This script is used to find the attenuation at which the scanner can give both the 90 degree and 180 degree flip angle

The script takes two or more arguments, run the script with the following command:
python calAtten.py <table_name> <file_path1> <file_path2> ...
where the table is the name that you called the table that contains the scanner amplitudes when you first ran the scan in Tecmag
and the file_path is the path to the tnt file at a certain attenuation value. you can include as many tnt files as you want

the output will return a small range in which the attenuation value that gives both the 90 degree and 180 degree flip angle likely occurs
it also plots the R^2 values for the 3rd and 4th order polynomial fits for the maximum signal intensity vs amplitude values at each attenuation value
on the plot, the intersection of the two curves is likely the attenuation value that gives both the 90 degree and 180 degree flip angle

this script find the maximum signal intensity for each scanner amplitude for each scan at an attenuation value. It then takes the 
maximum signal intensity vs scanner amplitude for each scan at an attenuation value as a function of scanner amplitudes 
and fits it to both 3rd order and 4th order polynomials. It takes the r2 value of the fits and plots them as a function of attenuation value.

This script assumes that the ideal curve produced by the scanner is a 4th order polynomial where the two peaks represent the amplitudes at which the 90 and 
180 degree flip angles occur. However it takes into consideration of the case where the true attenuation at which this occurs is between the values of 
attenuation tested.
"""

import sys
import numpy as np
from lowfieldGUI.pytnt_2025.pytnt.processTNT import TNTfile
import matplotlib.pyplot as plt
import re
from scipy.optimize import fsolve

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

def findPeaks(file_path):
    """
    finds the scanner amplitude that gives the maximum signal amplitude and most power
    """
    tnt = TNTfile(file_path)

    fid_data = tnt.DATA
    fid_data.dtype
    type('complex64')

    signal_peaks = np.zeros(fid_data.shape[1])
    signal_peaks.dtype = np.complex64 # initializing 

    for i in range(fid_data.shape[1]):
        signal_peaks[i] = np.max(fid_data[:, i, 0, 0])        

    return signal_peaks

def readAtnVal(file_path):

    """
    Searches the last 100 lines of the file for the first instance of 'f1atten'
    followed by a specific control character pattern and returns the number that follows as a float.
    """
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None

    # Check last 100 lines of the file
    last_lines = lines[-100:]
    last_section = ''.join(last_lines)

    # Pattern:
    # f1atten followed by up to 4 NULs, STX, up to 4 NULs, then the number, then EOT
    pattern = fr'f1atten(?:[\x00]{{0,4}}\x02[\x00]{{0,4}})(\d+)\x04'

    match = re.search(pattern, last_section)
    if match:
        try:
            return float(match.group(1))
        except ValueError:
            print("Matched something but couldn't convert to float.")
            return None

    print("No attenuation value found in the last 100 lines.")
    return None

def find_intersection(x_vals, y_vals1, y_vals2):
    # Find the two points for each line
    i1 = np.argmin(y_vals1)  # Find the index of the minimum y value for y_vals1
    i2 = np.argmin(y_vals2)  # Find the index of the minimum y value for y_vals2
    
    x1, y1 = x_vals[i1], y_vals1[i1]  # Point from the first dataset
    x2, y2 = x_vals[i2], y_vals1[i2]  # Another point from the first dataset

    x3, y3 = x_vals[i1], y_vals2[i1]  # Point from the second dataset
    x4, y4 = x_vals[i2], y_vals2[i2]  # Another point from the second dataset

    # Calculate the slopes (m1 and m2) of both lines
    m1 = (y2 - y1) / (x2 - x1)  # Slope of the line for y_vals1
    m2 = (y4 - y3) / (x4 - x3)  # Slope of the line for y_vals2

    # Calculate the intercepts (b1 and b2)
    b1 = y1 - m1 * x1  # Intercept of the line for y_vals1
    b2 = y3 - m2 * x3  # Intercept of the line for y_vals2

    # Set the two equations equal to each other to find the intersection
    # y1 = m1*x + b1  and  y2 = m2*x + b2
    # Solve for x: m1*x + b1 = m2*x + b2  -->  (m1 - m2)*x = b2 - b1
    if m1 != m2:
        x_intersect = (b2 - b1) / (m1 - m2)
        y_intersect = m1 * x_intersect + b1  # You can also compute y by plugging x_intersect back into either line equation
        return x_intersect, y_intersect
    else:
        print("The lines are parallel and do not intersect.")
        return None


if len(sys.argv) < 2:
    print("Usage: calAtten.py <table_name> <file_path1> <file_path2> ...")
    sys.exit(1)

file_paths = sys.argv[2:]
table_name = sys.argv[1]
r2_3 = np.zeros(len(file_paths))
r2_4 = np.zeros(len(file_paths))
attenuation_vals = np.zeros(len(file_paths))
i = 0

for fp in file_paths:
    scanner_amplitudes = readAmpTbl(table_name, fp)
    signal_peaks = findPeaks(fp)
    attenuation_vals[i] = readAtnVal(fp)
    
    # find the 3rd and 4th order polynomials that fit the signal_peaks and scanner_amplitude data
    betas3 = np.polyfit(scanner_amplitudes, signal_peaks, 3)
    betas4 = np.polyfit(scanner_amplitudes, signal_peaks, 4)
    poly3 = np.poly1d(betas3)
    poly4 = np.poly1d(betas4)
    x_fit = np.linspace(min(scanner_amplitudes), max(scanner_amplitudes), len(scanner_amplitudes))
    y_fit3 = poly3(x_fit)
    y_fit4 = poly4(x_fit)

    
    #find the R^2 value for the 3rd and 4th order polynomials at each attenuation value and store in r2_3 and r2_4
    r2_3[i] = np.real(np.sum((signal_peaks - y_fit3)**2) / np.sum((signal_peaks - np.mean(signal_peaks))**2))
    r2_4[i] = np.real(np.sum((signal_peaks - y_fit4)**2) / np.sum((signal_peaks - np.mean(signal_peaks))**2))

    i += 1

# Define the domain of interest between the two minimization points
start_index = min(np.argmin(r2_3), np.argmin(r2_4))
end_index = max(np.argmin(r2_3), np.argmin(r2_4))

# Slice the arrays to consider only the region between the minimization points
domain_attenuation = attenuation_vals[start_index:end_index+1]
domain_r2_3 = r2_3[start_index:end_index+1]
domain_r2_4 = r2_4[start_index:end_index+1]

# Calculate the absolute difference between the two curves within the domain
differences = np.abs(domain_r2_3 - domain_r2_4)

# Find the indices of the two smallest differences within the domain
smallest_diff_indices = np.argsort(differences)[:2]

# Get the corresponding attenuation values for the smallest differences
attenuation_1 = domain_attenuation[smallest_diff_indices[0]]
attenuation_2 = domain_attenuation[smallest_diff_indices[1]]

x_intersect, y_intersect = find_intersection(domain_attenuation, domain_r2_3, domain_r2_4)
x_intersect = np.abs(x_intersect)

# Print the results
print(f"The attenuation value that gives you both the 90 degree and 180 degree flip angle likely occurs between attenuation values: {attenuation_1} and {attenuation_2}")
print(f"The approximate attenuation value that gives you both the 90 degree and 180 degree flip angle is {x_intersect:.2f} dB")

# Plotting the curves with the domain of interest

plt.plot(attenuation_vals, np.real(r2_3), label='R^2 values for 3rd order polynomial', color='blue')
plt.plot(attenuation_vals, np.real(r2_4), label='R^2 values for 4th order polynomial', color='red')
plt.axvline(x=attenuation_1, color='black', linestyle='--', label=f'Outer bounds of attenuation range')
plt.axvline(x=attenuation_2, color='black' , linestyle='--')
plt.scatter(x_intersect, y_intersect, color='black', label='Intersection of R^2 values for 3rd and 4th order polynomials', zorder=6, s=15)
plt.legend()
plt.xlabel('Attenuation value')
plt.ylabel('R^2 value')
plt.title('Intersection of R^2 values for 3rd and 4th order polynomials')
plt.show()