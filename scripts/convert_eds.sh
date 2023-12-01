#!/bin/bash

paths=("/eos/user/e/eegidiop/lorenzettiCom/datasets/zee/prod0000.092023.10k.nopileup.V0/ESD/Zee.ESD.root.0" \
       "/eos/user/e/eegidiop/lorenzettiCom/datasets/zee/prod0001.102023.50k.nopileup.V0/ESD/zee.ESD.root"   \
       "/eos/user/e/eegidiop/lorenzettiCom/datasets/zee/prod0002.102023.100k.nopileup.V0/ESD/zee.ESD.root"  \
       "/eos/user/e/eegidiop/lorenzettiCom/datasets/zee/prod0003.102023.100k.nopileup.V0/ESD/zee.ESD.root"  \
       "/eos/user/e/eegidiop/lorenzettiCom/datasets/zee/prod0004.102023.100k.nopileup.V0/ESD/zee.ESD.root"
       )

cd $HOME/l0_ringer/src/eds_parser
mkdir $HOME/l0_ringer/data/

for i in ${!paths[@]}; do
    mkdir $HOME/l0_ringer/data/data_$i
    mkdir $HOME/l0_ringer/data/data_$i/jobs
    mkdir $HOME/l0_ringer/data/data_$i/events
    python3 $HOME/l0_ringer/src/eds_parser/create_jobs.py -i ${paths[$i]} -o $HOME/l0_ringer/data/data_$i/events -j $HOME/l0_ringer/data/data_$i/jobs/
    nohup python3 $HOME/l0_ringer/src/eds_parser/read_eds.py -j $HOME/l0_ringer/data/data_$i/jobs/ > $HOME/l0_ringer/data/data_$i/log.txt &
done