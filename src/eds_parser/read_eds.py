# -*- coding: utf-8 -*-

import ROOT

import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, '../lorenzetti_utils/')
sys.path.insert(1, '../')

from lorenzetti_utils.EventStore import EventStore
import argparse
import pandas as pd
import tqdm
import os
import multiprocessing

# usage: python read_eds.py --input file.root --output file.csv

event = None

def read_events(*args):
    """
    Read EDS.ROOT file and return a pandas DataFrame with the data.
    """
    global event
    path, start, end = args[0]
    print("Reading events from %d to %d." %(start, end))

    # Create a dictionary with the data
    cells = {}
    keys = ["eta", "phi", "e", "et", "delta_phi", "delta_e", "entry_idx", "sampling", "detector"]

        
    for key in keys:
        cells[key] = []

    total_entries = range(start, end+1)
    for entry in total_entries:
        event.GetEntry(entry)
        cells_container = event.retrieve("CaloCellContainer_Cells")
        descriptor_container = event.retrieve("CaloDetDescriptorContainer_Cells")

        cell_idx = 0
        while True: #for cell_idx in range(cells_container.size()):
            try:
                cell = cells_container.at(cell_idx)
            except:
                break
            else:
                cell_idx += 1
                cells["eta"].append(float(cell.eta))
                cells["phi"].append(float(cell.phi))
                cells["e"].append(float(cell.e))
                cells["et"].append(float(cell.et))
                cells["delta_phi"].append(float(cell.dphi))
                cells["delta_e"].append(float(cell.deta))
                cells["entry_idx"].append(int(entry))

                det = descriptor_container.at(int(cell.descriptor_link))
                cells["sampling"].append(int(det.sampling))
                cells["detector"].append(int(det.detector))
                #cells["cells"].append(Cell(det.e, det.et, det.eta, det.phi, det.sampling))

                assert (det.eta == cell.eta and det.phi == cell.phi and det.e == cell.e and cell.deta == det.deta and cell.dphi == det.dphi)

    print("Done reading events from %d to %d." %(start, end))

    # Create a pandas DataFrame
    df = pd.DataFrame(cells)

    return df

def launch_subprocesses(path):
    global event

    event = EventStore(path, "CollectionTree")
    total_entries = event.GetEntries()

    NUM_WORKERS = 1000

    # split the work
    ranges = [(path, i*total_entries//NUM_WORKERS, (i+1)*total_entries//NUM_WORKERS) for i in range(NUM_WORKERS)]

    # launch the subprocesses
    with multiprocessing.Pool(NUM_WORKERS) as pool:
        df_results = pool.map(read_events, ranges)
    
    return pd.concat(df_results)

if __name__ == "__main__":

    # parse arguments
    parser = argparse.ArgumentParser(description='Ferramenta para conversão de arquivos EDS.ROOT de simulação a nível de célula em conjuntos de dados binários.\n\
                                    Ferramenta desenvolvida por Leandro A. (leandro@lps.ufrj.br)', prog="python read_eds.py")

    parser.add_argument('-i', '--input', type=str, help='Input file.', required=True)
    parser.add_argument('-o', '--output', type=str, help='Output file.', required=True)

    arguments = parser.parse_args()

    # read EDS.ROOT file
    df = launch_subprocesses(arguments.input)

    if not os.path.exists(arguments.output):
        os.makedirs("".join(arguments.output.split("/")[:-1]))
    
    print(df.head())

    # save to CSV
    try:
        df.to_csv(arguments.output, index=False)
    except:
        print("Error while saving to CSV file.")
    else:
        print("File saved to %s." %arguments.output)