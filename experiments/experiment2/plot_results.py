import numpy as np
import Levenshtein

def benchmark(answer_file_name, ground_truth_file_name):
    print(answer_file_name)

    with open(answer_file_name) as f:
        reconstructed_strands = f.readlines()

    reconstructed_strands = list(map(lambda x:x.strip(), reconstructed_strands))


    answer_file = open(ground_truth_file_name,"r")

    answer = answer_file.readlines()
    answer = list(map(lambda x:x.strip(), answer))

    total_answer_length = 0

    print(len(reconstructed_strands), len(answer))


    offset = 0

    total_num_bases = 0
    total_edit_dist = 0
    total_num_strands = 0
    total_errors = 0
    for i in range(len(answer)):
        total_num_strands += 1
        total_edit_dist += Levenshtein.distance(reconstructed_strands[i-offset], answer[i])
        total_num_bases += len(answer[i])
        for j in range(len(answer[i])):
            if j>= len(reconstructed_strands[i-offset]):
                total_errors+= len(answer[i]) - len(reconstructed_strands[i-offset])
                break
            elif reconstructed_strands[i-offset][j] != answer[i][j]:
                total_errors+= 1


    hamming_distance = total_errors / len(answer)
    edit_distance = total_edit_dist / len(answer)




    # # Below For Plotting Error Rate
    correct = 0
    for i in range(len(reconstructed_strands)):
        if answer[i] == reconstructed_strands[i]:
            correct+= 1
        #else:
            #print(i)
            #print('Actual:\t',answer[i])
            #print('Recon: \t', reconstructed_strands[i])

    index_wrong_counts = [0]*len(answer[0])
    for i in range(len(reconstructed_strands)):
        for j in range(len(answer[0])):
            if j >= len(reconstructed_strands[i]):
                index_wrong_counts[j] += 1
                continue
            #print(i,j)
            #print(len(reconstructed_strands[i]),len(answer[i]))
            #print(answer[i])
            if reconstructed_strands[i][j] != answer[i][j]:
                index_wrong_counts[j] += 1

    import matplotlib.pyplot as plt
    import numpy as np
    


    xpoints = list(range(len(answer[0])))
    ypoints = list(map(lambda x: x/len(reconstructed_strands), index_wrong_counts))

    success_rate = correct / len(answer)
    return hamming_distance, edit_distance, success_rate, (xpoints, ypoints)

import pandas as pd
import matplotlib.pyplot as plt
import pathlib
import seaborn as sns

sns.set_style("whitegrid")

tool_names = ["MUSCLE", "Trellis BMA", "ITR", "BBS"]
tool_filename_identifier = ["muscle_output.txt", "trellis_bma_output.txt", "itr_output.txt", "bbs_output.txt"]

ground_truth_file_name = "../datasets/Centers_subsampled.txt"
output_file_dir = "../results/experiment2/"

success_rates_dict = {}
hamming_distances_dict = {}

import numpy as np

for cluster_size in np.linspace(2, 30, 15, dtype=int):
    hamming_distances = []
    edit_distances = []
    success_rates = []

    for i in range(len(tool_names)):
        answer_file_name = pathlib.Path(output_file_dir) / f"cluster_size_{cluster_size}" / tool_filename_identifier[i]
        hamming_distance, edit_distance, success_rate, _ = benchmark(answer_file_name, ground_truth_file_name)
        hamming_distances.append(hamming_distance)
        edit_distances.append(edit_distance)
        success_rates.append(success_rate)
        print(success_rate)

    # Put the results in a pandas dataframe
    df = pd.DataFrame({"Tool": tool_names, "Hamming Distance": hamming_distances, "Edit Distance": edit_distances, "Success Rate": success_rates})
    print(df)

    success_rates_dict[cluster_size] = success_rates
    hamming_distances_dict[cluster_size] = hamming_distances

# Plot the success rates vs. cluster size for each tool
plt.figure(figsize=(5, 4))
for i in range(len(tool_names)):
    #failure_rates = [1 - success_rates_dict[cluster_size][i] for cluster_size in success_rates_dict]
    #plt.plot(list(success_rates_dict.keys()), failure_rates, label=tool_names[i], marker='o')
    hamming_distances = [hamming_distances_dict[cluster_size][i] for cluster_size in hamming_distances_dict]
    plt.plot(list(hamming_distances_dict.keys()), hamming_distances, label=tool_names[i], marker='o')
plt.xlabel("Coverage")
plt.ylabel("Average Hamming Distance")
plt.yscale("log")
plt.tight_layout()
plt.legend()
plt.savefig("../results/experiment2/hamming_dist_vs_coverage.pdf")
plt.show()


plt.figure(figsize=(5, 4))
for i in range(len(tool_names)):
    failure_rates = [1 - success_rates_dict[cluster_size][i] for cluster_size in success_rates_dict]
    plt.plot(list(success_rates_dict.keys()), failure_rates, label=tool_names[i], marker='o')
    
plt.xlabel("Coverage")
plt.ylabel("Failure Rate")
plt.yscale("log")
plt.tight_layout()
plt.legend()
plt.savefig("../results/experiment2/failure_rate_vs_coverage.pdf")
plt.show()

