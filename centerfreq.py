import sys
import numpy as np
from lowfieldGUI.pytnt_2025.pytnt.processTNT import TNTfile


## Perform a frequency sweep or frequency detection routine
# call the Tecmag software to do that, would need a write function?
# save the data from the Tecmag software as a .tnt file

## Read the data from the TNT file
if len(sys.argv) < 2:
    print("Usage: python centerfreq.py <tnt_file_name>")
    sys.exit(1)

tnt_file_name = sys.argv[1]
tnt = TNTfile(tnt_file_name)

fid_data = tnt.DATA
# The first dimension represents the number of data points in the FID.
# The second dimension represents the number of coils or receive channels.
# The third dimension represents the number of scans or repetitions.
# The fourth dimension represents the number of datasets or experiments.
fid_data.dtype
type('complex64')
fid_data.shape
(16384, 1, 1, 1)

signal_amp = fid_data[:, 0, 0, 0]

## The Fourier-transformed spectrum data
freq_ppm = tnt.freq_ppm()
# freq_ppm is a numpy array of the frequency in ppm
freq_ppm.dtype
type('float64')
freq_ppm.shape
(16384,)

freq_Hz = tnt.freq_Hz()
# freq_Hz is a numpy array of the frequency in Hz
freq_Hz.dtype
type('float64')
freq_Hz.shape
(16384,)

## Find the center frequency from the spectrum data

# find max amplitude
max_amp_complex = np.max(signal_amp)
max_amp_absolute = np.max(np.abs(signal_amp))

#get index of maximum amplitude
max_index = np.argmax(signal_amp)

#center freq is the frequency at which the maximum signal amplitude is detected.
center_freq_ppm = freq_ppm[max_index]
center_freq_Hz = freq_Hz[max_index]

print("the center frequency in ppm is: ", center_freq_ppm)
print("the center frequency in Hz is: ", center_freq_Hz)