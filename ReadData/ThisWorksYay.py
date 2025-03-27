from pytnt_2025 import TNTfile

tnt = TNTfile('GrapefruitTNT/SE_grapefruit_500avgs_2.tnt')
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

