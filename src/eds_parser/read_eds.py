# -*- coding: utf-8 -*-

import ROOT

import sys, os

sys.path.insert(1, '../lorenzetti_utils/')
sys.path.insert(1, '../')

from lorenzetti_utils.EventStore import EventStore
import argparse
import pandas as pd
import tqdm
import pickle

# usage: python read_eds.py --jobs_path <path_to_jobs_dir>

def read_events(event_obj, start, end):
    """
    Read EDS.ROOT file and return a pandas DataFrame with the data.
    """

    # Create a dictionary with the data
    cells = {}
    keys = ["eta", "phi", "e", "et", "delta_phi", "delta_eta", "entry_idx", "sampling", "detector"]

        
    for key in keys:
        cells[key] = []

    total_entries = range(start, end+1)
    with tqdm.tqdm(total=len(total_entries)) as pbar:
        for entry_idx in total_entries:

            event_obj.GetEntry(entry_idx)
            cells_container = event_obj.retrieve("CaloCellContainer_Cells")
            descriptor_container = event_obj.retrieve("CaloDetDescriptorContainer_Cells")

            num_cells = len(cells_container)
            for cell_idx in range(num_cells):
                try:
                    cell = cells_container.at(cell_idx)
                except:
                    break
                else:
                    cells["eta"].append(float(cell.eta))
                    cells["phi"].append(float(cell.phi))
                    cells["e"].append(float(cell.e))
                    cells["et"].append(float(cell.et))
                    cells["delta_phi"].append(float(cell.dphi))
                    cells["delta_eta"].append(float(cell.deta))
                    cells["entry_idx"].append(int(entry_idx))

                    det = descriptor_container.at(int(cell.descriptor_link))
                    cells["sampling"].append(int(det.sampling))
                    cells["detector"].append(int(det.detector))
                    #cells["cells"].append(Cell(det.e, det.et, det.eta, det.phi, det.sampling))
                    pbar.set_description("Processing cell %d/%d of entry %d" %(cell_idx, num_cells, entry_idx))

                    assert (det.eta == cell.eta and det.phi == cell.phi and det.e == cell.e and cell.deta == det.deta and cell.dphi == det.dphi)

            pbar.update(1)
    # Create a pandas DataFrame
    df = pd.DataFrame(cells)

    return df

def tune_job(job_path):
    '''
    Read job from a path and return a pandas DataFrame with the data.
    '''
    with open(job_path, "rb") as job_file:
        job_data = pickle.load(job_file)

    if job_data['job_status'] == 'DONE':
        return
        
    df = read_events(job_data['events'], job_data['lim_inf'], job_data['lim_sup'])

    try:
        old_df = pd.read_csv(job_data['outpath'], index_col=0)
    except FileNotFoundError:
        df.to_csv(job_data['outpath'])
    else:
        new_df = pd.concat([old_df, df], ignore_index=True)
        new_df.to_csv(job_data['outpath'])

    job_data['job_status'] = 'DONE'

    # dump job
    with open(job_path, "wb") as job_file:
        pickle.dump(job_data, job_file)

    print('Job %03d processed.' %job_data['job_id'])

if __name__ == "__main__":

    # parse arguments
    parser = argparse.ArgumentParser(description='Ferramenta para conversão de arquivos EDS.ROOT de simulação a nível de célula em conjuntos de dados binários.\n\
                                    Ferramenta desenvolvida por Leandro A. (leandro@lps.ufrj.br)', prog="python read_eds.py")

    parser.add_argument('-j', '--jobs_path', type=str, help='Path to jobs to be tunned.', required=True)

    arguments = parser.parse_args()

    # read events from the jobs
    for filename in os.scandir(arguments.jobs_path):
        if not filename.is_file():
            continue

        tune_job(filename.path)