#!/bin/bash

mkdir -p ../results/ablation_study

clusters_list=("../datasets/BinnedNanoporeTwoFlowcells_clusters_subsampled.txt" 
               "../datasets/oligo0_UnderlyingClusters.txt" 
               "../datasets/Clusters_removed_empty_cluster.txt")
centers_list=("../datasets/BinnedNanoporeTwoFlowcells_centers_subsampled.txt" 
              "../datasets/oligo0refs.txt" 
              "../datasets/Centers_removed_empty_cluster.txt")
read_lengths=(140 108 110)
output_directory=("../results/ablation_study/sabary" 
                  "../results/ablation_study/chandak" 
                  "../results/ablation_study/microsoft_CNR")
separator=("===" "CLUSTER" "===")

for i in 0 1 2
do
    mkdir -p ${output_directory[i]}
    echo "Running tools on ${clusters_list[i]} and ${centers_list[i]}"
    ./bbs-dbg -i ${clusters_list[i]} -l ${read_lengths[i]}  -s ${separator[i]} > ${output_directory[i]}/bbs_dbg_weight_output.txt
    ./bbs -i ${clusters_list[i]} -l ${read_lengths[i]}  -s ${separator[i]} -a 0 > ${output_directory[i]}/bbs_no_laplace_smoothing_output.txt
    ./bbs -i ${clusters_list[i]} -l ${read_lengths[i]}  -s ${separator[i]} -S 1 > ${output_directory[i]}/bbs_unidirectional_output.txt
    ./bbs -i ${clusters_list[i]} -l ${read_lengths[i]}  -s ${separator[i]} -S 1 -b 1 > ${output_directory[i]}/bbs_greedy_output.txt
done