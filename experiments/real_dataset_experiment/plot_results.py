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
        #    print(i)
        #    print('Actual:\t',answer[i])
        #    print('Recon: \t', reconstructed_strands[i])

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

experiment_names = ["sabary", "microsoft_CNR", "chandak"]
dataset_dir = "../datasets/"

ground_truth_file_list = [pathlib.Path(dataset_dir) / "BinnedNanoporeTwoFlowcells_centers_subsampled.txt",
                          pathlib.Path(dataset_dir) / "Centers_removed_empty_cluster.txt",
                          pathlib.Path(dataset_dir) / "oligo0refs.txt"]
output_file_dir = "../results/real_dataset_experiment/"

tool_names = ["MUSCLE", "Trellis BMA", "ITR", "CPL", "BBS"]
tool_filename_identifier = ["muscle_output.txt", "trellis_bma_output.txt", "itr_output.txt", "cpl_output.txt", "bbs_output.txt"]

error_rates = {}

for i in range(len(experiment_names)):
    experiment_name = experiment_names[i]
    ground_truth_file_name = ground_truth_file_list[i]
    hamming_distance_list = []
    edit_distance_list = []
    success_rate_list = []
    error_rate_list = []
    for j, tool_name in enumerate(tool_names):
        answer_file_name = pathlib.Path(output_file_dir) / experiment_name / tool_filename_identifier[j] #f"{output_file_dir}output_{experiment_name}/{tool_filename_identifier[i]}"
        hamming_distance, edit_distance, success_rate, error_points = benchmark(answer_file_name, ground_truth_file_name)
        hamming_distance_list.append(hamming_distance)
        edit_distance_list.append(edit_distance)
        success_rate_list.append(success_rate)
        error_rate_list.append(error_points)

    error_rates[experiment_name] = error_rate_list
    #print(error_rate_list)
    print("\n")
    # Create a DataFrame to store the results
    results_df = pd.DataFrame({
        'Tool': tool_names,
        'Hamming Distance': hamming_distance_list,
        'Edit Distance': edit_distance_list,
        'Success Rate': success_rate_list
    })

    # Print the DataFrame
    print(results_df)

import seaborn as sns
sns.set(style="whitegrid")
# Set color palette for better distinction between lines
#sns.set_palette("colorblind", n_colors=len(tool_names))
experiment_id = ["Bar-Lev et al.", "Srinivasavaradhan et al.", "Chandak et al."]


# Plotting with added frame and thicker lines
#plt.figure(figsize=(12, 3))
fig, axs = plt.subplots(1, 3, figsize=(12, 3))

for idx, experiment_name in enumerate(experiment_names):
    xpoints, ypoints = error_rates[experiment_name][0]  # Assuming all tools have the same xpoints

    for tool_idx, tool_name in enumerate(tool_names):
        _, ypoints = error_rates[experiment_name][tool_idx]
        axs[idx].plot(xpoints, ypoints, label=tool_name, linewidth=2.5)

    
    axs[idx].set_title(f'{experiment_id[idx]}')
    if idx == 1:
        axs[idx].set_xlabel('Position in strand')
    if idx == 0:
        axs[idx].set_ylabel('Error Rate')

# Adjust the layout to make space for the legend on the right
plt.subplots_adjust(right=0.85, wspace=0.3, bottom=0.2)

# Use a common yrange
#for ax in axs:
#    ax.set_ylim(0, 0.3)

# Create a single legend on the right of the subplots
handles, labels = axs[0].get_legend_handles_labels()
print(handles, labels)
fig.legend(handles, labels, loc='center right', title='Tool')

plt.savefig("../results/error_rates.pdf")
plt.show()