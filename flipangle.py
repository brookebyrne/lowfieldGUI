# This script calculates the flip angle of a shaped pulse.
# Uses adapted code from https://www.mathworks.com/matlabcentral/fileexchange/37122-tnmr-gui 
# Code is adapted from MATLAB code into python code and edited to correct for the off-resonance frequency in the lab's magnet
import sys
import re
import numpy as np
from lowfieldGUI.pytnt_2025.pytnt.processTNT import TNTfile
import matplotlib.pyplot as plt
import time

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

def center_freq(file_path, table_name):

    tnt = TNTfile(file_path)

    fid_data = tnt.DATA
    fid_data.dtype
    type('complex64')

    scanner_amp_vals = read_amplitude_table(file_path, table_name)

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

# start_time = time.time()

# Read tnt file
if len(sys.argv) < 2:
    print("Usage: python flipangle.py <tnt_file_name>")
    sys.exit(1)

file_path = sys.argv[1]
table_name = sys.argv[2]

tnt = TNTfile(file_path)

## The Fourier-transformed spectrum data
freq_ppm = tnt.freq_ppm() # freq_ppm is a numpy array of the frequency in ppm
freq_ppm.dtype
type('float64')
freq_ppm.shape
(16384,)

freq_Hz = tnt.freq_Hz() # freq_Hz is a numpy array of the frequency in Hz
freq_Hz.dtype
type('float64')
freq_Hz.shape
(16384,)

# Find the best scanner amplitude
best_scanner_amp = center_freq(file_path, table_name)

# def shaped_pulse_b1(rf_shape, dt, flip_angle, off_res_freq, gamma, phase_table=None):
#     """
#     Finds the peak B1 (in Gauss) value of the shaped pulse ignoring relaxation.
    
#     Currently only works for flip_angle <= 180 degrees.
    
#     Output:
#     peakB1: The maximum B1 value of a shaped pulse that gives the desired flip angle.
    
#     Inputs:
#     rf_shape: The pulse shape you are using.
#     dt: The time per point of the pulse. Example: a 10 ms pulse width with 128 points has dt of 78 microseconds. dt must be in seconds.
#     flip_angle: The desired flip angle in degrees.
#     off_res_freq: The off-resonance frequency in Hz.
#     gamma: Gyromagnetic ratio in Hz/Gauss, change based on nucleus
#     phase_table (optional): If provided, only the absolute value of rf_shape is used. If not provided, the function assumes that rf_shape > 0 is 0 phase and rf_shape < 0 is π phase.
#     """
    
#     if flip_angle < 0.1 or flip_angle > 180:
#         raise ValueError('Flip angle must be between 0 and 180 degrees')
    
#     if phase_table is None:
#         phase_table = np.zeros_like(rf_shape)
#         phase_table[rf_shape < 0] = np.pi
#     else:
#         if len(phase_table) != len(rf_shape):
#             raise ValueError('Phase table must have the same length as rf_shape')
    
#     rabi_freq = np.arange(10, 2001, 5)  # This should be more than a big enough range. In Hz!
#     target = np.abs(np.sin(np.deg2rad(flip_angle)))
    
#     if target == 0:
#         return 0
    
#     mz = np.zeros_like(rabi_freq)
#     mt = np.zeros_like(rabi_freq)

#     for i, freq in enumerate(rabi_freq):
#         m = shaped_pulse(rf_shape, dt, freq, off_res_freq, phase_table)
#         mt[i] = np.abs(m[0] + 1j * m[1])
#         mz[i] = np.abs(m[2])
        
#         if flip_angle <= 90 and (mt[i] >= target):
#             val_m = np.abs(mt[i] - target)
#             val_m1 = np.abs(mt[i-1] - target)
            
#             if val_m > val_m1:
#                 peak_b1 = rabi_freq[i-1] / gamma
#             else:
#                 peak_b1 = rabi_freq[i] / gamma
#             break
        
#         elif (mz[i] < 0 and (mt[i] < target)) or (i == len(rabi_freq) - 1):
#             val_m = np.abs(mt[i] - target)
#             val_m1 = np.abs(mt[i-1] - target)
            
#             if val_m > val_m1:
#                 peak_b1 = rabi_freq[i-1] / gamma
#             else:
#                 peak_b1 = rabi_freq[i] / gamma
#             break
    
#     return peak_b1

# def shaped_pulse(rf_shape, dt, rabi_freq, off_res_freq, phase_table=None):
#     """
#     Calculates the magnetization vector after applying an arbitrary pulse shape.
#     Starting magnetization is assumed to be along the Z-axis.

#     Given a vector of RF amplitudes ranging from 0 to 100 (or -100 to 100),
#     this function will apply square pulses of length dt and peak w1 frequency,
#     rabi_freq, to a spin with an off-resonance frequency, off_res_freq, and
#     return the resulting magnetization. Relaxation is ignored.

#     Inputs:
#     rf_shape: Vector of RF amplitudes. Negative values will be interpreted as
#               pulses with π phase.
#     dt: Length of each segment of the pulse sequence in seconds.
#     rabi_freq: The peak w1 frequency of the pulse, i.e., the w1 frequency in Hz
#                at amplitude 100.
#     off_res_freq: Off-resonance frequency in Hz.
#     phase_table (optional): If provided, any signs on rf_shape are ignored. The
#                            phase table should be entered in radians. This allows
#                            for completely arbitrary phase control.

#     Output:
#     M: The final magnetization vector [Mx, My, Mz].
#     """
    
#     rf_shape = np.array(rf_shape)
#     dt = float(dt)
#     rabi_freq = float(rabi_freq)
#     off_res_freq = float(off_res_freq)

#     if phase_table is None:
#         phase_table = np.zeros_like(rf_shape)
#         phase_table[rf_shape < 0] = np.pi
#         rf_shape = np.abs(rf_shape) / 100
#     else:
#         if len(phase_table) != len(rf_shape):
#             raise ValueError('Phase table must have the same length as rf_shape')
#         rf_shape = np.abs(rf_shape) / 100

#     m = np.array([0, 0, 1])

#     for i in range(len(rf_shape)):
#         m = _arb_rot(rabi_freq * rf_shape[i], dt, off_res_freq, phase_table[i]) @ m

#     return m

# def _arb_rot(rabi_freq, dt, off_res_freq, phase):
#     """
#     Calculates the arbitrary rotation matrix for a shaped pulse.

#     Outputs:
#     rot_matrix: The rotation matrix for a shaped pulse.

#     Inputs:
#     rabi_freq: The peak w1 frequency of the pulse, i.e., the w1 frequency in Hz at amplitude 100.
#     dt: Length of each segment of the pulse sequence in seconds.
#     off_res_freq: Off-resonance frequency in Hz.
#     phase: The phase of the pulse in radians.

#     """
#     omega = np.sqrt(rabi_freq**2 + off_res_freq**2)
#     sin_omega_dt = np.sin(omega * dt)
#     cos_omega_dt = np.cos(omega * dt)

#     a = rabi_freq / omega * sin_omega_dt
#     b = off_res_freq / omega * sin_omega_dt
#     c = cos_omega_dt

#     rot_matrix = np.array([[c - a * np.cos(phase), -b - a * np.sin(phase), 0],
#                            [b - a * np.sin(phase), c + a * np.cos(phase), 0],
#                            [0, 0, 1]])

#     return rot_matrix

# # Find center frequency 
# center_freq_Hz, center_freq_ppm = center_freq(tnt_file_name)

# print("center freq", center_freq_Hz)
# # Calculate necessary parameters in calling the shaped_pulse_b1 function
# duration = tnt.fid_times()[-1]
# dt = duration / tnt.actual_npts[0] #not sure if this is correctly defined
# off_res_freq = center_freq_Hz + tnt.freq_offset()
# gamma = 42.58  # Gyromagnetic ratio in Hz/Gauss, change based on nucleus

# # Calculate the peak B1 field amplitude  
# peak_b1 = shaped_pulse_b1(signal_amp, dt, 90, off_res_freq, gamma, phase_table=None)
# print("peak b1",peak_b1)

# # Calculate the flip angle
# # θ = γ × B₁ × t 
# #       Where:
# #       B₁ is the amplitude of the applied RF pulse
# #       t is the duration of the RF pulse
# #       γ is the gyromagnetic ratio of the nucleus being imaged
# flip_angle_rad = gamma * peak_b1 * dt
# flip_angle_deg = np.rad2deg(flip_angle_rad)

# print(f"The flip angle is {flip_angle_deg} degrees or {flip_angle_rad} radians")

# end_time = time.time()
# print(f"Time taken: {end_time - start_time} seconds")