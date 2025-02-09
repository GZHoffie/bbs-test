import numpy as np
from Levenshtein import distance, editops

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

def analyze(clusters, centers):
    num_del = 0
    num_ins = 0
    num_sub = 0
    num_traces = 0
    for cluster, center in zip(clusters, centers):
        num_traces += len(cluster)
        for read in cluster:
            ops = editops(read, center)
            if len(ops) > 0:
                num_del += (np.array(ops)[:,0] == 'delete').sum()
                num_ins += (np.array(ops)[:,0] == 'insert').sum()
                num_sub += (np.array(ops)[:,0] == 'replace').sum()
    
    p_del = num_del/(num_traces*len(centers[0]))
    p_ins = num_ins/(num_traces*len(centers[0]))
    p_sub = num_sub/(num_traces*len(centers[0]))

    print(f"Deletion rate: {p_del}")
    print(f"Insertion rate: {p_ins}")
    print(f"Substitution rate: {p_sub}")
    print(f"Total error rate: {p_del + p_ins + p_sub}")
    print(f"Number of clusters: {len(clusters)}")
    print(f"Average number of traces per cluster: {num_traces/len(clusters)}")



if __name__ == "__main__":
    #clusters, centers = input_file("./Clusters_removed_empty_cluster.txt", "./Centers_removed_empty_cluster.txt")
    clusters, centers = input_file("./oligo0_UnderlyingClusters.txt", "./oligo0refs.txt", "CLUSTER", skip_first_line=True)
    #clusters, centers = input_file("/mnt/c/Users/zhenh/trace_recon/oligo0_UnderlyingClusters.txt", "/mnt/c/Users/zhenh/trace_recon/oligo0refs.txt", "CLUSTER", skip_first_line=True)

    analyze(clusters, centers)

            
            
