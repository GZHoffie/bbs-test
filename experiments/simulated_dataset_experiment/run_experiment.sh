#!/bin/bash

mkdir -p ../results/simulated_dataset_experiment

for i in ../datasets/simulated_data/*.txt
do
    # Get the stem of the filename
    filename=$(basename -- "$i")
    filename="${filename%.*}"

    # Get the substring after the first underscore
    test_name="${filename#*_}"


    echo "Running tools on ${test_name}"
    python3 run_all.py -i $i -c ../datasets/simulated_data/EncodedStrands.txt -l 110 -o ../results/simulated_dataset_experiment/${test_name} -s "CLUSTER" -b 0.03 -d 0.02 -n 0.02 --bbs --muscle --trellis-bma --itr --cpl
done