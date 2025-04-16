import os
from pathlib import Path

def Read_Tecmag_Header(filename=None):
    header = {}
    if filename is None:
        filename = os.path.join(os.path.dirname(__file__), os.path.basename(os.path.splitext(input("Enter Tecmag NMR data file path: "))[0] + ".tnt"))
    
    if os.path.exists(filename) and os.path.getsize(filename) > 1056:
        with open(filename, 'rb') as file_pt:
            Hdr_var = Read_Tecmag_hdr(file_pt)
            Hdr_name = Hdr_var[:, 0:28].tolist()
            Hdr_offset = [eval(x) for x in Hdr_var[:, 28:34].tolist()]
            Hdr_type = [x.strip() for x in Hdr_var[:, 35:43].tolist()]
            Hdr_size = [eval(x) for x in Hdr_var[:, 44:47].tolist()]
            Hdr_desc = Hdr_var[:, 47:85].tolist()

            for i, (Var_name, Var_offset, Var_type, Var_size, Var_desc) in enumerate(zip(Hdr_name, Hdr_offset, Hdr_type, Hdr_size, Hdr_desc)):
                file_pt.seek(Var_offset)
                Var_data = file_pt.read(Var_size)
                if Var_type == 'char' and Var_size > 1:
                    Var_data = Var_data.decode().rstrip('\x00')
                else:
                    Var_data = Var_data
                header[Var_name.strip()] = Var_data
    return header

def Read_Tecmag_hdr(file_pt):
    # Implement the logic to read the header from the file_pt
    pass