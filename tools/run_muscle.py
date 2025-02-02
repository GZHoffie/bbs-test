# Adopted from https://github.com/MLI-lab/noisy_dna_data_storage/blob/master/LSH_clustering.ipynb

from Bio import AlignIO
import subprocess
import operator

def multiple_alignment_muscle(cluster,out=False):
    # write cluster to file
    file = open("clm.fasta","w")
    for i,c in enumerate(cluster):
        file.write(">S%d\n" % i)
        file.write(c)
        file.write("\n")
    file.close()

    muscle_exe = r"/home/zhenhao/bbs-test/tools/muscle-linux-x86.v5.3" # assuming you've already put this in the main directory
    output_alignment = "clmout.fasta"
    subprocess.run([muscle_exe, "-align", "clm.fasta", "-output", output_alignment], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    msa = AlignIO.read(output_alignment, "fasta")
    if out:
        print(msa)
    alignedcluster = []
    for i in msa:
        alignedcluster += [i.seq]
    return alignedcluster

def majority_merge(reads,weight = 0.4):
    # assume reads have the same length
    res = ""
    for i in range(len(reads[0])):
        counts = {'A':0,'C':0,'G':0,'T':0,'-':0,'N':0}
        for j in range(len(reads)):
            counts[reads[j][i]] +=1
        counts['-'] *= weight
        mv = max(counts.items(), key=operator.itemgetter(1))[0]
        if mv != '-':
            res += mv
    return res

def align_clusters(clusters, output_file):
    ### align clusters, generate candidates
    with open(output_file, "w") as f:
        for i, clusterinds in enumerate(clusters):
            
            ma = multiple_alignment_muscle(clusterinds)
            res = majority_merge(ma)
            f.write(res + "\n")
                
            if i % 100 == 0:
                print("%",round(i*100/len(clusters),2),"of the clusters are aligned.")







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


if __name__ == "__main__":
    import sys
    import subprocess
    import argparse

    parser = argparse.ArgumentParser(description="Run MUSCLE alignment on clusters.")
    parser.add_argument("-i", "--input", required=True, help="Path to the cluster file.")
    parser.add_argument("-c", "--center", required=True, help="Path to the center file.")
    parser.add_argument("-o", "--output", required=True, help="Path to the output file.")
    parser.add_argument("-s", "--separator", default="===", help="Separator used in the cluster file.")

    args = parser.parse_args()

    print("Running Muscle")

    clusters, centers = input_file(args.input, args.center, args.separator)
    align_clusters(clusters, args.output)
