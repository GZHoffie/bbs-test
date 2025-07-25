# Scripts for downloading and using the state-of-the-art Trace Reconstruction tools

## MUSCLE

Download MUSCLE v5 using the following command

```bash
# under tools/ directory
wget https://github.com/rcedgar/muscle/releases/download/v5.3/muscle-linux-x86.v5.3
chmod +x ./muscle-linux-x86.v5.3
```

Replace line 16 of `run_muscle.py` with the path to the MUSCLE executable, in my case, `"/home/zhenhao/bbs-test/tools/muscle-linux-x86.v5.3"`. The code used for trace reconstruction using MUSCLE is adopted from Antkowiak et al. [[1](https://github.com/MLI-lab/noisy_dna_data_storage/blob/master/LSH_clustering.ipynb)]. The MUSCLE program can then be run using

```bash
python run_muscle.py [-h] -i INPUT -c CENTER -o OUTPUT [-s SEPARATOR]
```

## Trellis BMA

Download and setup the Trellis BMA repository.

```bash
# under tools/ directory
git clone https://github.com/microsoft/TrellisBMA.git

# get the absolute path of the TrellisBMA directory
cd TrellisBMA
pwd
```

Copy output of `pwd` to the third line of `run_trellis_bma.py`. In my case, the path is `'/home/zhenhao/bbs-test/tools/TrellisBMA/'`. Trellis BMA can then be run using the following command

```bash
python run_trellis_bma.py [-h] -i INPUT -c CENTER -o OUTPUT [-s SEPARATOR] -l READ_LENGTH -b SUBSTITUTION_RATE -d DELETION_RATE -n INSERTION_RATE
```

## Iterative algorithm

Download and setup the ITR algorithm.

```bash
# under tools/ directory
git clone https://github.com/omersabary/Reconstruction.git
cd Reconstruction/Iterative

# Compile the files
g++ -std=c++0x -O3 -g3 -Wall -c -fmessage-length=0 -o LCS2.o LCS2.cpp
g++ -std=c++0x -O3 -g3 -Wall -c -fmessage-length=0 -o EditDistance.o EditDistance.cpp
g++ -std=c++0x -O3 -g3 -Wall -c -fmessage-length=0 -o Clone.o Clone.cpp
g++ -std=c++0x -O3 -g3 -Wall -c -fmessage-length=0 -o Cluster2.o Cluster2.cpp
g++ -std=c++0x -O3 -g3 -Wall -c -fmessage-length=0 -o LongestPath.o LongestPath.cpp
g++ -std=c++0x -O3 -g3 -Wall -c -fmessage-length=0 -o CommonSubstring2.o CommonSubstring2.cpp
g++ -std=c++0x -O3 -g3 -Wall -c -fmessage-length=0 -o DividerBMA.o DividerBMA.cpp
g++ -std=c++0x -O3 -g3 -Wall -c -fmessage-length=0 -o DNA.o DNA.cpp
g++ -o DNA *.o
```

Again, replace line 14 of `run_ITR.py` with the path to the executable of ITR algorithm. In may case it is `/home/zhenhao/bbs-test/tools/Reconstruction/Iterative/DNA`.

Iterative algorithm requires special treatments for the input and output. The input format is required to be like the [following](https://github.com/omersabary/Reconstruction/blame/main/Iterative/README.md).

```
Ground truth sequence 1
**** 
Strand 1 in cluster
Strand 2 in cluster 
Strand 3 in cluster
// Blank row - End of cluster 
// Blank row -  End of cluster 
Ground truth sequence 1
**** 
Strand 1 in cluster
Strand 2 in cluster 
Strand 3 in cluster
// Blank row - End of cluster 
// Blank row -  End of cluster 
```
which requires both the ground truth and the clusters to be present in the input file. Once the input is parsed to the above format, the ITR algorithm can be run using

```bash
python run_ITR.py [-h] -i INPUT_FILE -d OUTPUT_DIRECTORY -o OUTPUT_FILE
```


Moreover, the output of the ITR algorithm is split into `OUTPUT_DIRECTORY/output-results-fail.txt` and `OUTPUT_DIRECTORY/output-results-success.txt`. We write a script in `run_all.py` to parse the output files so that the output format is consistent with the other tools.


## CPL algorithm

Download and setup the CPL algorithm.

```bash
# under tools/ directory
git clone https://github.com/itaiorr/Deep-DNA-based-storage.git
cd Deep-DNA-based-storage/CPL

# In the file Graph.cpp, add a line `#include <climits>`.
# remove the original compilation files 
rm *.o main
make
chmod +x ./main
```


## BBS algorithm

Download the BBS executable from GitHub releases.

```bash
# under tools/ directory
wget https://github.com/GZHoffie/bbs/releases/download/v0.0.1/bbs
chmod +x ./bbs
```

BBS can be run using the following.

```bash
./bbs [-h] -i INPUT -s SEPARATOR -l READ_LENGTH > OUTPUT_FILE
```

## Collective script to run all tools

We create a script to run all tools.

# References

[1] Antkowiak, Philipp L., et al. "Low cost DNA data storage using photolithographic synthesis and advanced information reconstruction and error correction." *Nature communications* 11.1 (2020): 5345.