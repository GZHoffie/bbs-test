import numpy as np

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


def sample(clusters, centers, output_cluster_file, output_center_file, num_clusters, num_sample_per_cluster=None, minimum_coverage=None, separator = "==="):
    print("Before limiting minimum coverage:", len(clusters))
    if minimum_coverage is not None:
        small_clusters = [i for i in range(len(clusters)) if len(clusters[i]) < minimum_coverage]
        centers = [centers[i] for i in range(len(centers)) if i not in small_clusters]
        clusters = [clusters[i] for i in range(len(clusters)) if i not in small_clusters]
    
    print("After limiting minimum coverage:", len(clusters))

    # Randomly choose num_samples samples from the clusters
    if len(clusters) > num_clusters:
        chosen_indices = np.random.choice(len(clusters), num_clusters, replace=False)
    else:
        chosen_indices = np.arange(len(clusters))
    
    
    chosen_clusters = [clusters[i] for i in chosen_indices if len(clusters[i]) > 0]
    chosen_centers = [centers[i] for i in chosen_indices if len(clusters[i]) > 0]



    if num_sample_per_cluster is not None:
        for i in range(len(chosen_clusters)):
            if len(chosen_clusters[i]) > num_sample_per_cluster:
                chosen_clusters[i] = np.random.choice(chosen_clusters[i], num_sample_per_cluster, replace=False)

    with open(output_cluster_file, "w") as f:
        f.write(separator + "\n")
        for cluster in chosen_clusters:
            for element in cluster:
                f.write(element + "\n")
            f.write(separator + "\n")
    
    with open(output_center_file, "w") as f:
        for center in chosen_centers:
            f.write(center + "\n")


if __name__ == "__main__":
    #clusters, centers = input_file("/mnt/c/Users/zhenh/trace_recon/our_nanopore_UnderlyingClusters.txt", "/mnt/c/Users/zhenh/trace_recon/our_nanopore_refs.txt", "CLUSTER", skip_first_line=True)
    #num_samples = 1500

    #sample(clusters, centers, "/mnt/c/Users/zhenh/trace_recon/our_nanopore_UnderlyingClusters_subsampled.txt", "/mnt/c/Users/zhenh/trace_recon/our_nanopore_refs_subsampled.txt", num_samples, num_sample_per_cluster=25, separator = "===")

    # Subsample the Sabary et al dataset
    """
    num_samples = 10000
    clusters, centers = input_file("datasets/BinnedNanoporeTwoFlowcells_clusters.txt",
                                      "datasets/BinnedNanoporeTwoFlowcells_centers.txt", skip_first_line=False, seperator="===")
    sample(clusters, centers, "datasets/BinnedNanoporeTwoFlowcells_clusters_subsampled.txt", "datasets/BinnedNanoporeTwoFlowcells_centers_subsampled.txt", num_samples, separator = "===")
    """
    

    # Subsample the Microsoft CNR dataset
    num_samples = 500

    clusters, centers = input_file("datasets/Clusters_removed_empty_cluster.txt",
                                   "datasets/Centers_removed_empty_cluster.txt", skip_first_line=True, seperator="===")
    
    # Sample at most 1000 clusters with at least 60 samples per cluster
    sample(clusters, centers, "datasets/Clusters_subsampled.txt", "datasets/Centers_subsampled.txt", num_samples, minimum_coverage=50, separator = "===")

    clusters, centers = input_file("datasets/Clusters_subsampled.txt",
                                   "datasets/Centers_subsampled.txt", skip_first_line=True)

    # Create subsampled datasets for nanopore reads
    for num_reads in reversed([2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]):
        
        sample(clusters, centers, f"datasets/Clusters_subsampled_{num_reads}.txt", f"datasets/Centers_subsampled_{num_reads}.txt", num_samples, num_sample_per_cluster=num_reads, separator = "===")
        clusters, centers = input_file(f"datasets/Clusters_subsampled_{num_reads}.txt",
                                       f"datasets/Centers_subsampled_{num_reads}.txt", skip_first_line=True)
    


    