# Datasets for Benchmark Experiments

## Download Test datasets

In our benchmark, we test three separate nanopore read clusters: one from our in-house synthesized and sequenced clusters, and two open-source datasets from Srinivasavaradhan et al. [[1](https://github.com/microsoft/clustered-nanopore-reads-dataset)] and Chandak et al. [[2](https://github.com/shubhamchandak94/nanopore_dna_storage)].

1. The Microsoft CNR dataset by Srinivasavaradhan et al. is available at [this repository](https://github.com/microsoft/clustered-nanopore-reads-dataset), and can be downloaded using

   ```bash
   git clone https://github.com/microsoft/clustered-nanopore-reads-dataset
   ```

2. The in-house dataset and the dataset by Chandak et al. use the perfect clustering: all sequenced reads are mapped to the closest sequence in the ground truth. 

All datasets are avilable in the [Google drive](https://drive.google.com/drive/folders/1NXzimFt2tFtpw2XfqyWX6dXYJml_pPyw?usp=sharing). In the shared folder, `[Clusters/Centers]_removed_empty_cluster` correspond to the Microsoft CNR dataset with the empty clusters removed, `our_nanopore_*.txt` correspond to the in-house dataset, and `oligo0*.txt` correspond to the Chandak et al. dataset.

## Dataset Processing

 - **Removing empty clusters and subsampling**: Since some tools may report an error given empty clusters, and some tools are very slow given large clusters, we remove the empty clusters for the Microsoft CNR dataset and perform subsampling for the in-house dataset using the script [`subsample_dataset.py`](./subsample_dataset.py).

 - **Check info on the dataset**: We also provide script to check the insertion/deletion/substitution rate as well as coverage of a dataset in [`analyze_dataset.py`](./analyze_dataset.py). The related information returned by the script is summarized as follows.

 |Dataset Name|Insertion Rate|Deletion Rate|Substitution Rate|Error Rate|Number of Clusters|Average Coverage|
 |------------|--------------|-------------|-----------------|----------|------------------|------------|
 In-house|5.26%|2.17%|4.68%|12.11%|1496|24.15|
 Microsoft CNR|2.14%|1.86%|1.77%|5.77%|9984|27.01|
 Chandak et al.|4.56%|5.09%|3.91%|13.56%|1466|114.29|


# References
[1] Srinivasavaradhan, Sundara Rajan, et al. "Trellis BMA: Coded trace reconstruction on IDS channels for DNA storage." *2021 IEEE International Symposium on Information Theory (ISIT)*. IEEE, 2021.

[2] Chandak, Shubham, et al. "Overcoming high nanopore basecaller error rates for DNA storage via basecaller-decoder integration and convolutional codes." *ICASSP 2020-2020 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)*. IEEE, 2020.