#!/bin/bash

# usage: source convert_esd <output_base_path> <numero_eventos_por_job> <-verbose>

paths=("/eos/user/e/eegidiop/lorenzettiCom/datasets/zee/prod0000.092023.10k.nopileup.V0/ESD/Zee.ESD.root" \
       "/eos/user/e/eegidiop/lorenzettiCom/datasets/zee/prod0001.102023.50k.nopileup.V0/ESD/zee.ESD.root"   \
       "/eos/user/e/eegidiop/lorenzettiCom/datasets/zee/prod0002.102023.100k.nopileup.V0/ESD/zee.ESD.root"  \
       "/eos/user/e/eegidiop/lorenzettiCom/datasets/zee/prod0003.102023.100k.nopileup.V0/ESD/zee.ESD.root"  \
       "/eos/user/e/eegidiop/lorenzettiCom/datasets/zee/prod0004.102023.100k.nopileup.V0/ESD/zee.ESD.root"
       )

date_time=$(date +"%d-%m-%Y")


cd $HOME/l0_ringer/src/esd_parser
mkdir $1/$date_time
mkdir $1/$date_time/data

for i in ${!paths[@]}; do
    mkdir $1/$date_time/data/data_$i
    mkdir $1/$date_time/data/data_$i/jobs
    mkdir $1/$date_time/data/data_$i/events

    if [ -z "$3" ]; then
        log_file=/dev/null
    else
        log_file=$1/$date_time/data/data_$i/log
    fi

    python3 $HOME/l0_ringer/src/esd_parser/create_jobs.py -i ${paths[$i]} -o $1/$date_time/data/data_$i/events/ -j $1/$date_time/data/data_$i/jobs/ --events_per_job $2 > $log_file 2>&1 &
    nohup python3 $HOME/l0_ringer/src/esd_parser/read_esd.py -j $1/$date_time/data/data_$i/jobs/ > $log_file 2>&1 &
done