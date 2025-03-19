#!/bin/bash

# Run the tools. Make sure this script is run under the bbs-test/tools/ directory.
clusters_list=("../datasets/BinnedNanoporeTwoFlowcells_clusters_subsampled.txt" 
               "../datasets/oligo0_UnderlyingClusters.txt" 
               "../datasets/Clusters_removed_empty_cluster.txt")
centers_list=("../datasets/BinnedNanoporeTwoFlowcells_centers_subsampled.txt" 
              "../datasets/oligo0refs.txt" 
              "../datasets/Centers_removed_empty_cluster.txt")
read_lengths=(140 108 110)
output_directory=("../results/real_dataset_experiment/sabary" 
                  "../results/real_dataset_experiment/chandak" 
                  "../results/real_dataset_experiment/microsoft_CNR")
separator=("===" "CLUSTER" "===")

# Trellis BMA with the default parameters actually performs better than the trained parameters.
substitution_rate=(0.03 0.03 0.03)
deletion_rate=(0.02 0.02 0.02)
insertion_rate=(0.02 0.02 0.02)

#substitution_rate=(0.0468 0.0391 0.0177)
#deletion_rate=(0.0217 0.0509 0.0186)
#insertion_rate=(0.0526 0.0456 0.0214)


for i in 0 1 2
do
    echo "Running tools on ${clusters_list[i]} and ${centers_list[i]}"
    python3 run_all.py -i ${clusters_list[i]} -c ${centers_list[i]} -l ${read_lengths[i]} -o ${output_directory[i]} -s ${separator[i]} -b ${substitution_rate[i]} -d ${deletion_rate[i]} -n ${insertion_rate[i]} --bbs --muscle --trellis-bma --itr --cpl
    #./bbs -i ${clusters_list[i]} -l ${read_lengths[i]} -s ${separator[i]} -d 1 2> test.txt
done