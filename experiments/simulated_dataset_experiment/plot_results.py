import numpy as np


cluster_size_list = [10, 20, 30, 40, 50, 60]
error_rate_list = 0.01 * np.array([1, 2, 3, 4, 5, 6])
small_cluster_size_list = [2, 4, 6, 8, 10]

import Levenshtein

def benchmark(answer_file_name, ground_truth_file_name):

    with open(answer_file_name) as f:
    #with open("/home/zhenhao/greedy-align/output.txt") as f:
        reconstructed_strands = f.readlines()

    reconstructed_strands = list(map(lambda x:x.strip(), reconstructed_strands))


    #reconstructed_strands = # your reconstructed strands go here
    #answer_file = open("/mnt/c/Users/zhenh/trace_recon/oligo0refs.txt","r")
    #answer_file = open("/home/zhenhao/greedy-align/experiments/experiment0/EncodedStrands.txt","r")
    #answer_file = open("/home/zhenhao/greedy-align/experiments/data/clustered-nanopore-reads-dataset/Centers_removed_empty_cluster.txt","r")
    answer_file = open(ground_truth_file_name,"r")

    answer = answer_file.readlines()
    answer = list(map(lambda x:x.strip(), answer))

    total_answer_length = 0


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


    hamming_distance = total_errors / total_num_bases
    edit_distance = total_edit_dist / total_num_bases




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


ground_truth_file_name = "../datasets/simulated_data/EncodedStrands.txt"
output_file_dir = "../results/simulated_dataset_experiment/"

tool_names = ["MUSCLE", "Trellis BMA", "ITR", "CPL", "BBS"]
tool_filename_identifier = ["muscle_output.txt", "trellis_bma_output.txt", "itr_adjusted_output.txt", "cpl_output.txt", "bbs_output.txt"]

# Find the values for Small Cluster Size
import pandas as pd
import seaborn as sns

small_cluster_results_hamming = {tool: [] for tool in tool_names}
small_cluster_results_edit = {tool: [] for tool in tool_names}
small_cluster_results_success = {tool: [] for tool in tool_names}

for cluster_size in small_cluster_size_list:
    for i, tool_name in enumerate(tool_names):
        answer_file_name = output_file_dir + "SmallCluster_" + str(cluster_size) + "/" + tool_filename_identifier[i]
        hamming_distance, edit_distance, success_rate, (xpoints, ypoints) = benchmark(answer_file_name, ground_truth_file_name)

        small_cluster_results_hamming[tool_name].append(hamming_distance)
        small_cluster_results_edit[tool_name].append(edit_distance)
        small_cluster_results_success[tool_name].append(success_rate)

df_small_cluster_hamming = pd.DataFrame(small_cluster_results_hamming, index=small_cluster_size_list)
df_small_cluster_edit = pd.DataFrame(small_cluster_results_edit, index=small_cluster_size_list)
df_small_cluster_success = pd.DataFrame(small_cluster_results_success, index=small_cluster_size_list)

print("Hamming Distance DataFrame:")
print(df_small_cluster_hamming)
print("\nEdit Distance DataFrame:")
print(df_small_cluster_edit)
print("\nSuccess Rate DataFrame:")
print(df_small_cluster_success)






# Find the values for Error Rate
error_rate_results_hamming = {tool: [] for tool in tool_names}
error_rate_results_edit = {tool: [] for tool in tool_names}
error_rate_results_success = {tool: [] for tool in tool_names}

for error_rate in error_rate_list:
    for i, tool_name in enumerate(tool_names):
        answer_file_name = output_file_dir + "ErrorRate_" + str(error_rate) + "/" + tool_filename_identifier[i]
        hamming_distance, edit_distance, success_rate, (xpoints, ypoints) = benchmark(answer_file_name, ground_truth_file_name)

        error_rate_results_hamming[tool_name].append(hamming_distance)
        error_rate_results_edit[tool_name].append(edit_distance)
        error_rate_results_success[tool_name].append(success_rate)

df_error_rate_hamming = pd.DataFrame(error_rate_results_hamming, index=error_rate_list)
df_error_rate_edit = pd.DataFrame(error_rate_results_edit, index=error_rate_list)
df_error_rate_success = pd.DataFrame(error_rate_results_success, index=error_rate_list)

print("Hamming Distance DataFrame:")
print(df_error_rate_hamming)
print("\nEdit Distance DataFrame:")
print(df_error_rate_edit)
print("\nSuccess Rate DataFrame:")
print(df_error_rate_success)




import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style='whitegrid')

fig, axes = plt.subplots(1, 2, figsize=(9, 5))
plt.rcParams['lines.markersize'] = 10  # Increase marker size for all plots

# Plot success rate w.r.t. small cluster size
markers = ['o', 's', '^', 'v', 'P']  # Different markers for each line
for idx, (col, marker) in enumerate(zip(df_small_cluster_success.columns, markers)):
    sns.lineplot(ax=axes[0], data=df_small_cluster_success[col], marker=marker, linewidth=2.5, linestyle='-', label=col)
axes[0].set_title('Success Rate vs Small Cluster Size')
axes[0].set_xlabel('Small Cluster Size')
axes[0].set_ylabel('Success Rate')
#axes[0].legend_.remove()


# Plot success rate w.r.t. error rate
df_error_rate_success.index = df_error_rate_success.index * 3
for idx, (col, marker) in enumerate(zip(df_error_rate_success.columns, markers)):
    sns.lineplot(ax=axes[1], data=df_error_rate_success[col], marker=marker, linewidth=2.5, linestyle='-', label=col)
axes[1].set_title('Success Rate vs Error Rate in traces')
axes[1].set_xlabel('Error Rate')
axes[1].set_ylabel('Success Rate')
#axes[1].legend_.remove()

# Add a single legend for all three plots
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc='center left', bbox_to_anchor=(1, 0.5))

plt.tight_layout()
plt.savefig("../results/success_rate_vs_small_cluster_size_and_error_rate.pdf")
plt.show()
