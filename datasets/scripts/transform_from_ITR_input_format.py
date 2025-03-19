def parse_syntax_ITR_output(input_file):
    """
    Parse the input file to extract centers and clusters.

    Args:
        input_file (str): Path to the file containing the clusters and centers in the specified format.

    Returns:
        tuple: A tuple (clusters, centers) where:
               - clusters is a list of lists, where each inner list represents a cluster.
               - centers is a list of strings representing the centers.
    """
    centers = []
    clusters = []
    
    with open(input_file, "r") as f:
        lines = f.readlines()

    current_cluster = []
    reading_clusters = False
    for line in lines:
        stripped_line = line.strip()

        if "****" in stripped_line:
            # Separator between center and cluster elements
            reading_clusters = True
            continue
        elif stripped_line == "" and reading_clusters:
            reading_clusters = False
            # Empty line indicates the end of a cluster
            if current_cluster:
                clusters.append(current_cluster)
                current_cluster = []
        elif len(stripped_line) > 0:
            if not reading_clusters:
                # First non-empty line after a blank indicates a center
                centers.append(stripped_line)
            else:
                # Otherwise, it's part of the current cluster
                current_cluster.append(stripped_line)

    # Handle the last cluster if the file doesn't end with a blank line
    if current_cluster:
        clusters.append(current_cluster)

    return clusters, centers


def output_file(clusters, centers, cluster_file, center_file, separator="==="):
    
    with open(cluster_file, "w") as f:
        for cluster in clusters:
            for element in cluster:
                f.write(element + "\n")
            f.write(separator + "\n")
    
    with open(center_file, "w") as f:
        for center in centers:
            f.write(center + "\n")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Transform ITR input format to the format used in the dataset scripts")
    parser.add_argument("-i", "--input_file", type=str, required=True, help="Path to the input file")
    parser.add_argument("-c", "--cluster_file", type=str, required=True, help="Path to the output cluster file")
    parser.add_argument("-e", "--center_file", type=str, required=True, help="Path to the output center file")
    args = parser.parse_args()

    clusters, centers = parse_syntax_ITR_output(args.input_file)
    output_file(clusters, centers, args.cluster_file, args.center_file)