# Benchmark experiments

## Benchmarking the accuracy

We use the script [`./evaluate_answers.py`](./evaluate_answers.py) to evaluate the correctness of the reconstruction. You need the `Levenshtein` package to run the script, which can be installed with

```bash
pip install levenshtein
```

Run the script using 

```bash
python ./evaluate_answers.py -o <reconstruction_result_file> -a <ground_truth_file>
```

where both the `reconstruction_result_file` and `ground_truth_file` should be formatted with one sequence per line, similar to the [`Centers.txt`](https://github.com/microsoft/clustered-nanopore-reads-dataset/blob/main/Centers.txt) file in Microsoft CNR dataset.

Three metrics are reported:

1. `Hamming Distance`: the average hamming distance between the ground truth and the reconstruction.
2. `Edit Distance`: the average edit distance between the ground truth and the reconstruction.
3. `Success Rate`: percentage of clusters that are reconstructed successfully (0 hamming distance).

## Experiment 1

In the [experiment 1](./experiment1/) folder contains the script to run all the tools on real datasets.

After downloading data in the [datasets](../datasets/) folder, and setting up all the scripts in [tools](../tools/) folder, run the following

```bash
# assuming at bbs-test/ folder
cd tools
chmod +x ../experiments/experiment1/run_experiments.sh
../experiments/experiment1/run_experiments.sh
```

to run all the tools on all the datasets. The output is stored in `bbs-test/results/experiment1`. Then in the same directory (`bbs-test/tools`) run `python ../experiments/experiment1/plot_results.py` to get the figure in `bbs-test/results/experiment1/`.

## Experiment 2

In [experiment 2](./experiment2/) we evaluate the performance of the algorithms on various coverages. To do this, we subsample the Microsoft CNR dataset by running,

```bash
# assuming at bbs-test/ folder
python ./datasets/scripts/subsample_datasets.py
```

which creates a series of `Centers_subsampled_<x>.txt` and `Clusters_subsampled_<x>.txt`, representing the datasets where the cluser sizes are exactly `<x>`.

Next, we use the same procedure as experiment 1,

```bash
# assuming at bbs-test/ folder
cd tools
chmod +x ../experiments/experiment2/run_experiments.sh
../experiments/experiment2/run_experiments.sh
python ../experiments/experiment2/plot_results.py
```

to run the algorithms across all cluster sizes and plot the results. The output can be found in `results/experiment2/`.


