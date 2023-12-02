# -*- coding: utf-8 -*-

import pandas as pd
import gzip
import shutil
import os

import argparse
import tqdm

# usage: python3 to_bytestream.py -c <path to .csv dir> -o <base path for hex file>
# example: python3 to_bytestream.py -c /eos/user/l/lassisdo/eds_parser/02-12-2023/data/data_0/events -o /eos/user/l/lassisdo/eds_parser/02-12-2023/data/data_0/hex

def csv_to_hex(csv_path, hex_path):
    """
    Read a csv file and convert it to a hex file.
    """

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

    with tqdm.tqdm(total=len(df['entry_idx'].unique())) as pbar:
        for entry_idx in df['entry_idx'].unique():

            with open(hex_path+"event_%05d.hex" %entry_idx, 'wb') as hex_file:

                cells_from_entry = df[keys].loc[df['entry_idx'] == entry_idx]

                for cell_idx in range(len(cells_from_entry)):
                    pbar.set_description("Writing cell %05d/%05d from event %05d." %(cell_idx, len(cells_from_entry), entry_idx))
                    for key in keys:
                        if key in keys[:-2]: # se a key estiver entre eta e sampling (não incluindo sampling)
                            hex_file.write(cells_from_entry[key].iloc[cell_idx].astype('float32').tobytes())
                        else:
                            hex_file.write(cells_from_entry[key].iloc[cell_idx].astype('uint32').tobytes())
            
            # compress hex file
            compress_file(hex_path+"event_%05d.hex" %entry_idx)
            pbar.set_description("Compressing event %05d." %entry_idx)
            pbar.update(1)
    
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

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Convert csv to hex and compress both the files.')
    parser.add_argument('-c', '--csv_path', type=str, help='Path to csv file.', required=True)
    parser.add_argument('-o', '--out_path', type=str, help='Path to output file.', required=True)

    arguments = parser.parse_args()

    if arguments.csv_path[-1] != '/':
        arguments.csv_path += '/'

    if arguments.out_path[-1] != '/':
        arguments.out_path += '/'

    if not os.path.exists(arguments.out_path):
        os.makedirs(arguments.out_path)

    for filename in os.scandir(arguments.csv_path):
        if not filename.is_file() or filename.name[-4:] != ".csv":
            continue
        
        csv_to_hex(filename.path, arguments.out_path)