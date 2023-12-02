import pandas as pd
import gzip
import shutil
import os

import argparse

# read csv files and convert to .hex
# compact hexdump and csv
# provide hexdump

def csv_to_hex(csv_path, hex_path):
    try:
        df = pd.read_csv(csv_path, sep=';')
    except FileNotFoundError:
        print("File %s not found." %csv_path)
        return
    
    # values which will be converted to hex and allocated in sequential order
    #       eta     phi       e    delta_phi delta_eta  samp    detec
    # 0x 00000000 00000000 00000000 00000000 00000000 00000000 00000000 -> 7*4 bytes = 28 bytes -> 224 bits
    #keys = ["eta", "phi", "e", "delta_phi", "delta_eta", "sampling", "detector", "entry_idx"]
    # bytes are little endian

    keys = ["eta", "phi", "e", "delta_phi", "delta_eta", "sampling", "detector"]

    for entry_idx in df['entry_idx'].unique():

        with open(hex_path+"event_%05d.hex" %entry_idx, 'wb') as hex_file:

            cell_from_entry = df[keys].loc[df['entry_idx'] == entry_idx]

            for cell_idx in len(cell_from_entry):
                for key in keys:
                    if key in keys[:-2]: # se a key estiver entre eta e sampling (não incluindo sampling)
                        hex_file.write(cell_from_entry[key].iloc[cell_idx].astype('float32').tobytes())
                    else:
                        hex_file.write(cell_from_entry[key].iloc[cell_idx].astype('uint32').tobytes())
        
        # compress hex file
        compress_file(hex_path+"event_%05d.hex" %entry_idx)
    
    # compress csv file
    compress_file(csv_path)


def compress_file(file_path):
    """
    Compress a file using gzip.
    """
    with open(file_path, 'rb') as f_in:
        with gzip.open(file_path+'.gpg', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    
    # delete uncompressed file
    os.remove(file_path)

if __name__ == "__main":

    parser = argparse.ArgumentParser(description='Convert csv to hex and compress both the files.')
    parser.add_argument('-c', '--csv_path', type=str, help='Path to csv file.', required=True)
    parser.add_argument('-o', '--out_path', type=str, help='Path to output file.', required=True)

    arguments = parser.parse_args()

    csv_to_hex(arguments.csv_path, arguments.out_path)