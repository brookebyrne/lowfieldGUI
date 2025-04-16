# calibrate the attenuation of the scanner
# this code assumes that you used the same scanner amplitude range for all of the scans at different attenuation values

import sys
import re
import numpy as np
from lowfieldGUI.pytnt_2025.pytnt.processTNT import TNTfile
import matplotlib.pyplot as plt
from calAmp import calAmp, readAmpTbl

#  needs to be able to take in multiple different tnt files, the table name after each file path.
# plot the fid with the amplitude table as the x axis, and y axis is signal max amplitude for each scanner ampltidue
#  in theory should be a straight line.
# find when the fid changes from being linear to not linear, that first peak is the attenuation that will 90 degree flip angle 
# the second peak is the attenuation will give you the 180 degree flip angle 
# amplitude table is gonna be 1-100 and then going to start at 60 db and decrease by steps of 6, 90 degree is at 30ish db, and 180 is afterwards.

# # check if correct amount of imputs
# if len(sys.argv) < 2:
#     print("Usage: python calAtn.py <amplitude_table_name> <tnt_file_path>")
#     sys.exit(1)

# table_name = sys.argv[1]
# scanner_amplitudes = readAmpTbl(table_name,sys.argv[2]) #again, assumes you are using same amp table for all fid scans

# flag = 0

# for i in range(len(sys.argv)-2):
#     file_path = sys.argv[2+i]
#     tnt = TNTfile(file_path)

#     fid_data = tnt.DATA
#     fid_data.dtype
#     type('complex64')

#     _, signal_peaks = calAmp(table_name, file_path)
#     for j in range(len(signal_peaks)):
#         if j == len(signal_peaks)-1:
#             break
#         elif signal_peaks[j] > signal_peaks[j+1]:
#             print(scanner_amplitudes[j])
#             print('90 degree flip angle at', scanner_amplitudes[j], 'dB and using the attenuation used in', file_path)
#             flag = 1
#             break

table_name = sys.argv[1]
file_path = sys.argv[2]

scanner_amplitudes = readAmpTbl(table_name, file_path) #again, assumes you are using same amp table for all fid scans

tnt = TNTfile(file_path)
fid_data = tnt.DATA
fid_data.dtype
type('complex64')

_, signal_peaks = calAmp(table_name, file_path)

plt.plot(scanner_amplitudes, signal_peaks)
plt.xlabel('Scanner Amplitude')
plt.ylabel('Signal Peak Amplitude')
plt.title(file_path)
plt.show()
plt.savefig(file_path + '.png')


for j in range(len(signal_peaks)):
    if j == len(signal_peaks)-1:
        print('attenuation is too high, no 90 degree flip angle not found')
        break
    elif signal_peaks[j] > signal_peaks[j+1]:
        print('90 degree flip angle found at', scanner_amplitudes[j], 'dB and using the attenuation used in', file_path)
        flag = 90
        break



