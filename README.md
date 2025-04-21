## Set up instructions 

Install pytnt by running the following command in your terminal:\
`gh repo clone brookebyrne/pytnt`

Install pytnt in your local disk by running the following command your terminal:\
`pip install "https://github.com/brookebyrne/pytnt"`

Rename submodule pytnt to pytnt_2025

## Simple usage

Read data from TNT file by running the following code

`import sys`
`from lowfieldGUI.pytnt_2025.pytnt.processTNT import TNTfile`
`import matplotlib.pyplot as plt`

`tnt_file_name = sys.argv[1]`
`tnt = TNTfile <tnt_file_name>`

`## The raw NMR FID data`
`fid_data = tnt.DATA`
`fid_data.dtype`
`type('complex64')`

`## The Fourier-transformed spectrum data`
`spec_data = tnt.freq_ppm()`
`spec_data.dtype`
`type('float64')`
`spec_data.shape`
`(16384,)`
`print(spec_data)`

`signal_amplitude = fid_data[:,0,0,0]`
`# Assumes the scanner only ran one FID at one amplitude value,`
`# If it ran multiple FIDs at different amplitude values, you would need to change the second dimension`
`# Plots signal amplitude`
`plt.plot(signal_amplitude)`

Calibrate the amplitude of the scanner by running the following code in your terminal;
`python calAmp.py <table_name> <file_path>`

    where table_name is the name of the table that contains the scanner amplitudes when you first ran the scan in Tecmag
    and file_path is the path to the tnt file

Calibrate the attenuation of the scanner by running the following code in your terminal;
`python calAtten.py <table_name> <file_path1> <file_path2> ...`

    where table_name is the name of the table that contains the scanner amplitudes when you first ran the scan in Tecmag
    and file_path1, file_path2, etc. are the paths to the tnt files at different attenuation values. You can include as many tnt files as you want

To test on exsiting files/data, run the following code:

`python calAmp.py rf1 C:\Users\bbyrn\lowfieldGUI\testFiles\FID_FA_cal.tnt`

`python calAtten.py rf1 C:\Users\bbyrn\lowfieldGUI\testFiles\FAcal18atten.tnt C:\Users\bbyrn\lowfieldGUI\testFiles\FAcal21atten.tnt C:\Users\bbyrn\lowfieldGUI\testFiles\FAcal24atten.tnt C:\Users\bbyrn\lowfieldGUI\testFiles\FAcal30atten.tnt C:\Users\bbyrn\lowfieldGUI\testFiles\FAcal33atten.tnt C:\Users\bbyrn\lowfieldGUI\testFiles\FAcal39atten.tnt C:\Users\bbyrn\lowfieldGUI\testFiles\FAcal42atten.tnt C:\Users\bbyrn\lowfieldGUI\testFiles\FAcal45atten.tnt C:\Users\bbyrn\lowfieldGUI\testFiles\FAcal48atten.tnt`



#outputs: attenuation, ampltiude, report how much power you are using 
#take the 250w power and apply the attenuation you want, (apply 3db then you get 125w) and then you can plot x axis to be 0-125w and y axis to be ? idk have to as charlotte on this oe

