# file to take output of read_tecmag.py to create an image using a fourier transform 
# make sure all the data is there, what variables do you need to run this function

import numpy as np
from scipy.fft import fft2, fftshift, ifft2
from ReadData.read_tecmag import read_tecmag  # Use absolute import

# Define dsize based on your data requirements
dsize = []  # Adjust this based on your specific needs

# Load data
data = read_tecmag('SE_grapefruit_500avgs_1.tnt', dsize)  # Pass dsize as an argument
SE_gfruit_data = np.abs(fftshift(ifft2(data)))

# Centering
shifted_data = np.roll(SE_gfruit_data, [11, 5], axis=(0, 1))

# Plot the shifted data
import matplotlib.pyplot as plt
plt.figure()
plt.imshow(shifted_data, cmap='gray')
plt.show()