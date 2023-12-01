# -*- coding: utf-8 -*-

import pickle
import argparse

import sys, os
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, '../lorenzetti_utils/')
sys.path.insert(1, '../')

from lorenzetti_utils.EventStore import EventStore

def create_jobs(root_filename, outpath, job_path, events_per_job=1000, tree_name="CollectionTree"):
    """
    Create a job for each "events_per_jobs" entries in the root file.
    """
    
    # read EDS.ROOT file
    events = EventStore(root_filename, tree_name)
    total_entries = events.GetEntries()

    num_jobs = int(total_entries/events_per_job)

    if not os.path.exists(job_path):
        os.makedirs(job_path)
        
    for job_idx in range(num_jobs):
        job = {
                "job_id": "%03d" %job_idx,
                "outpath": outpath,
                "job_status": "NOT STARTED",
                "lim_inf": job_idx*events_per_job,
                "lim_sup": (job_idx+1)*events_per_job,
                "events": events
            }
            
        with open("%s/job_%03d.pkl" %(job_path, job_idx), "wb") as f:
            pickle.dump(job, f)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Ferramenta para geração de jobs de conversão de eventos de célula em EDS para binario.', prog="python3 create_jobs.py")

    parser.add_argument('-i', '--input', type=str, help='Input file.', required=True)
    parser.add_argument('-o', '--output', type=str, help='Output file.', required=True)
    parser.add_argument('-j', '--jobs_path', type=str, help='Jobs output path.', required=True)
    parser.add_argument('-e', '--events_per_job', type=int, help='Number of events per job.', required=False, default=1000)
    parser.add_argument('-t', '--tree_name', type=str, help='Name of the tree in the root file.', required=False, default="CollectionTree")

    arguments = parser.parse_args()

    create_jobs(arguments.input, arguments.output, arguments.jobs_path, arguments.events_per_job, arguments.tree_name)

