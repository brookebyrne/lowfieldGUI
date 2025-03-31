## cd to lowfieldGUI directory: cd exsiting\path\lowfieldGUI
## RUN COMMAND IN TERMINAL: python ReadData\ThisWorksYay.py
import sys
from lowfieldGUI.pytnt_2025.pytnt.processTNT import TNTfile

if len(sys.argv) < 2:
    print("Usage: python read_tnt.py <tnt_file_name>")
    sys.exit(1)

tnt_file_name = sys.argv[1]
tnt = TNTfile(tnt_file_name)
## can change the file name to any other TNT file in the folder! yay

## The raw NMR FID data
fid_data = tnt.DATA

fid_data.dtype
type('complex64')
fid_data.shape
(16384, 1, 1, 1)

## The Fourier-transformed spectrum data
spec_data = tnt.freq_ppm()

spec_data.dtype
type('float64')
spec_data.shape
(16384,)

print(spec_data)

