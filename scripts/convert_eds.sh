#!/bin/bash

paths=("/eos/user/e/eegidiop/lorenzettiCom/datasets/zee/prod0000.092023.10k.nopileup.V0/ESD/Zee.ESD.root.0" \
         "/eos/user/e/eegidiop/lorenzettiCom/datasets/zee/prod0001.102023.50k.nopileup.V0/ESD/zee.ESD.root"   \
         "/eos/user/e/eegidiop/lorenzettiCom/datasets/zee/prod0002.102023.100k.nopileup.V0/ESD/zee.ESD.root"  \
         "/eos/user/e/eegidiop/lorenzettiCom/datasets/zee/prod0003.102023.100k.nopileup.V0/ESD/zee.ESD.root"  \
         "/eos/user/e/eegidiop/lorenzettiCom/datasets/zee/prod0004.102023.100k.nopileup.V0/ESD/zee.ESD.root")


for i in ${!paths[@]}; do
    echo "$HOME/l0_ringer/src/eds_parser/convert_eds.py ${paths[$i]} $HOME/l0_ringer/data_$i/readout.csv"
done