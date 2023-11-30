import ROOT
import argparse
import pandas as pd

# usage: python read_eds.py --input file.root --output file.csv

def read_events(path : str) -> pd.DataFrame:
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
    for idx, entry in enumerate(tree):
        branch = entry.GetBranch("CaloCellContainer_Cells")
        for cell in branch:
            cells["eta"].append(cell.eta)
            cells["phi"].append(cell.phi)
            cells["e"].append(cell.e)
            cells["et"].append(cell.et)
            cells["delta_phi"].append(cell.dphi)
            cells["delta_e"].append(cell.deta)
            cells["descr_idx"].append(cell.descriptor_link)
            cells["entry_idx"].append(idx)

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