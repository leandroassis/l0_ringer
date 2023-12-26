# -*- coding: utf-8 -*-

import pandas as pd
import gzip
import shutil
import os

import argparse
import tqdm

# usage: python3 to_bytestream.py -c <path to .csv> -o <base path for hex file>
# example: python3 to_bytestream.py -c /eos/user/l/lassisdo/esd_parser/02-12-2023/data/data_0/events/xxxx.csv -o /eos/user/l/lassisdo/esd_parser/02-12-2023/data/data_0/hex

def csv_to_hex(csv_path, hex_path, start, end, delete_source=False):
    """
    Read a csv file and convert it to a hex file.
    """

    try:
        df = pd.read_feather(csv_path, sep=';')
    except FileNotFoundError:
        print("File %s not found." %csv_path)
        return
    
    # values which will be converted to hex and allocated in sequential order
    #       eta     phi       e       samp     detec
    # 0x 00000000 00000000 00000000 00000000 00000000 -> 3*4 + 2*2 bytes = 16 bytes -> 128 bits
    #keys = ["eta", "phi", "e", "delta_phi", "delta_eta", "sampling", "detector", "entry_idx"]
    # bytes are little endian

    keys = ["eta", "phi", "e", "sampling", "detector"]

    num_iterations = len(df['entry_idx'].unique()) if (end == 0 and start == 0) else end-start
    with tqdm.tqdm(total=num_iterations) as pbar:
        for entry_idx in df['entry_idx'].unique():

            if entry_idx < start or entry_idx >= end:
                continue

            with open(hex_path+"event_%d.hex" %entry_idx, 'wb') as hex_file:

                cells_from_entry = df[keys].loc[df['entry_idx'] == entry_idx]

                for cell_idx in range(len(cells_from_entry)):
                    pbar.set_description_str("Writing cell %d/%d from event %d." %(cell_idx, len(cells_from_entry), entry_idx))
                    for key in keys:
                        if key in keys[:-2]: # se a key estiver entre eta e sampling (não incluindo sampling)
                            hex_file.write(cells_from_entry[key].iloc[cell_idx].astype('float32').tobytes())
                        else:
                            hex_file.write(cells_from_entry[key].iloc[cell_idx].astype('uint16').tobytes())
            
            # compress hex file
            compress_file(hex_path+"event_%d.hex" %entry_idx)
            pbar.set_description_str("Compressing event %d." %entry_idx)
            pbar.update(1)
    
    # compress csv file
    if delete_source:
        compress_file(csv_path, delete=False)


def compress_file(file_path):
    """
    Compress a file using gzip.
    """
    with open(file_path, 'rb') as f_in:
        with gzip.open(file_path+'.gz', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    
    # delete uncompressed file
    os.remove(file_path)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Convert csv to hex and compress both the files.')
    parser.add_argument('-c', '--csv_path', type=str, help='Path to csv file.', required=True)
    parser.add_argument('-o', '--out_path', type=str, help='Path to output file.', required=True)
    parser.add_argument('-s', '--start', type=int, help='Start index of the file.', required=False, default=0)
    parser.add_argument('-e', '--end', type=int, help='End index of the file.', required=False, default=0)
    parser.add_argument('-d', '--delete_source', type=bool, help='Delete csv file after conversion.', required=False, default=False)

    arguments = parser.parse_args()

    if arguments.out_path[-1] != '/':
        arguments.out_path += '/'

    if not os.path.exists(arguments.out_path):
        os.makedirs(arguments.out_path)
        
    csv_to_hex(arguments.csv_path, arguments.out_path, arguments.start, arguments.end, arguments.delete_source)