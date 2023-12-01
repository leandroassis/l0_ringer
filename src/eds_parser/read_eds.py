# -*- coding: utf-8 -*-

import ROOT
from EventStore import EventStore
import argparse
import pandas as pd
import tqdm

# usage: python read_eds.py --input file.root --output file.csv

def read_events(path):
    """
    Read EDS.ROOT file and return a pandas DataFrame with the data.
    """

    # Create a dictionary with the data
    cells = {}
    keys = ["eta", "phi", "e", "et", "delta_phi", "delta_e", "entry_idx", "sampling", "detector"]

        
    for key in keys:
        cells[key] = []

    event = EventStore(path, "CollectionTree")

    total_entries = range(event.GetEntries())
    with tqdm.tqdm(total=len(total_entries)) as pbar:
        for idx, entry in enumerate(total_entries):
            event.GetEntry(entry)
            cells_container = event.retrieve("CaloCellContainer_Cells")
            descriptor_container = event.retrieve("CaloDetDescriptorContainer_Cells")

            class Cell:
                def __init__( self, e, et, eta, phi, sampling ):
                    self.e = float(e); self.et = float(et); 
                    self.eta = float(eta); self.phi = float(phi); self.sampling = int(sampling)

            
            for cell_idx in range(cells_container.GetEntries()):

                cell = cells_container.at(cell_idx)

                cells["eta"].append(float(cell.eta))
                cells["phi"].append(float(cell.phi))
                cells["e"].append(float(cell.e))
                cells["et"].append(float(cell.et))
                cells["delta_phi"].append(float(cell.dphi))
                cells["delta_e"].append(float(cell.deta))
                cells["entry_idx"].append(int(idx))

                det = descriptor_container.at(cell.descriptor_link)
                cells["sampling"].append(int(det.sampling))
                cells["detector"].append(int(det.detector))
                #cells["cells"].append(Cell(det.e, det.et, det.eta, det.phi, det.sampling))
                pbar.set_description_str("Processing cell %d of entry %d." %(cell_idx, idx))

                assert (det.eta == cell.eta and det.phi == cell.phi and det.e == cell.e and det.et == cell.et and cell.deta == det.deta and cell.dphi == det.dphi)

            pbar.update(1)
    # Create a pandas DataFrame
    df = pd.DataFrame(cells)

    return df


if __name__ == "__main__":

    # parse arguments
    parser = argparse.ArgumentParser(description='Ferramenta para conversão de arquivos EDS.ROOT de simulação a nível de célula em conjuntos de dados binários.\n\
                                    Ferramenta desenvolvida por Leandro A. (leandro@lps.ufrj.br)', prog="python read_eds.py")

    parser.add_argument('-i', '--input', type=str, help='Input file.', required=True)
    parser.add_argument('-o', '--output', type=str, help='Output file.', required=True)

    arguments = parser.parse_args()
    print(arguments)
    print()

    # read EDS.ROOT file
    df = read_events(arguments.input)

    print(df.head())

    # save to CSV
    #df.to_csv(arguments.output, index=False)