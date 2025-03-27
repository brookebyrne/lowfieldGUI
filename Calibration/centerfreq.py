import sys
import os
import numpy 
from pytnt import TNTfile


# Perform a frequency sweep or frequency detection routine
#call the tecmag software to do that, would need a write function?


#read the the center frequency from the TNT file
read_tnt_file('FID_grapefruit_20avgs_1.tnt')
# the output of this is the spectrum data, which is a numpy array of the frequency and intensity and the FID date which 
#is a numpy array of the time and intensity

#center freq is the frequency at which the maximum signal intensity is detected.




#store center freq in a variable



def read_tnt_file(file):
    try:
        tnt_file = TNTfile(file)
        fid_data = tnt_file.DATA
        spec_data = tnt_file.freq_ppm()
    
        print("FID Data:")
        print(fid_data)
        print("Spectrum Data:")
        print(spec_data)
    
    except FileNotFoundError:
        print("Error: The file 'your_file.tnt' was not found.")
    except Exception as e:
         print(f"An error occurred: {e}")
    finally:
        if 'tnt_file' in locals() and hasattr(tnt_file, 'close'):
            tnt_file.close()