# -*- coding: utf-8 -*-

import ROOT
import argparse
import pandas as pd
#import tqdm

# usage: python read_eds.py --input file.root --output file.csv

def read_events(path):
    """
    Read EDS.ROOT file and return a pandas DataFrame with the data.
    """
    file = ROOT.TFile.Open(path)
    tree = file.CollectionTree

    # Create a dictionary with the data
    cells = {}
    keys = ["eta", "phi", "e", "et", "delta_phi", "delta_e", "descr_idx", "entry_idx"]
    for key in keys:
        cells[key] = []
    
    # Fill the dictionary
    #with tqdm.tqdm(total=tree.GetEntries()) as pbar:
    for idx, entry in enumerate(tree):
        branch = entry.GetBranch("CaloCellContainer_Cells")
        cells["eta"].append(branch.eta)
        cells["phi"].append(branch.phi)
        cells["e"].append(branch.e)
        cells["et"].append(branch.et)
        cells["delta_phi"].append(branch.dphi)
        cells["delta_e"].append(branch.deta)
        cells["descr_idx"].append(branch.descriptor_link)
        cells["entry_idx"].append(idx)
    #        pbar.update(1)

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