import numpy as np
import Levenshtein

def input_file(cluster_file, center_file, seperator="===", skip_first_line=True):
    # Read the cluster file and center file and return the clusters and centers
    centers = []
    clusters = []

    with open(cluster_file, "r") as f:
        if skip_first_line:
            f.readline()

        current_cluster = []
        for line in f.readlines():
            #print(line)
            if seperator in line:
                clusters.append(current_cluster.copy())
                #print(current_cluster)
                current_cluster = list()
            else:
                current_cluster.append(line.strip())
        
        if len(current_cluster) > 0:
            clusters.append(current_cluster)
    
    with open(center_file, "r") as f:
        for line in f.readlines():
            centers.append(line.strip())
        
    return clusters, centers


def edit_distance(center, cluster):
    # Return the list of edit distance
    for read in cluster:
        edit_distance = Levenshtein.distance(center, read)
        if edit_distance > 0.15*len(center):
            print(f"Center: {center}")
            print(f"Read:   {read}")
            print(f"Edit distance: {edit_distance}")
            print()
    return [Levenshtein.distance(center, read) for read in cluster]

def check_outliers(clusters, centers, threshold=0.1):
    # Check if there are any outliers in the clusters
    num_outliers = 0
    for i in range(len(clusters)):
        distances = edit_distance(centers[i], clusters[i])
        num_outliers += (np.array(distances) > threshold*len(centers[i])).sum()
    
    return num_outliers

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    edit_distance_dict = {}
    for cluster_size in [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24]:
        clusters, centers = input_file(f"../datasets/Clusters_subsampled_{cluster_size}.txt", f"../datasets/Centers_subsampled_{cluster_size}.txt")
        num_outliers = check_outliers(clusters, centers)
        print(f"Number of outliers for cluster size {cluster_size}: {num_outliers}, {num_outliers/len(clusters)}")

        edit_distance_dict[cluster_size] = [edit_distance(centers[i], clusters[i]) for i in range(len(clusters))]

        

    # Plot the edit distance
        # Plot the edit distance
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.boxplot([np.concatenate(edit_distance_dict[cluster_size]) for cluster_size in edit_distance_dict.keys()])
    ax.set_xticklabels(edit_distance_dict.keys())
    ax.set_xlabel('Cluster Size')
    ax.set_ylabel('Edit Distance')
    ax.set_title('Edit Distance by Cluster Size')
    plt.tight_layout()
    plt.show()

