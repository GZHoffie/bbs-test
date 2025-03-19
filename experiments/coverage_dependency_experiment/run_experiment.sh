#!/bin/bash

cluster_size=(2 4 6 8 10 12 14 16 18 20 22 24 26 28 30)

for i in {0..14}
do
    echo "Running tools on ${cluster_size[i]}"
    python3 run_all.py -i ../datasets/Clusters_subsampled_${cluster_size[i]}.txt -c ../datasets/Centers_subsampled_${cluster_size[i]}.txt -l 110 -o ../results/coverage_dependency_experiment/cluster_size_${cluster_size[i]} -s "===" -b 0.03 -d 0.02 -n 0.02 --bbs --muscle --trellis-bma --itr --cpl
done