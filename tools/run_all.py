import subprocess
import pathlib

def convert_ITR_input(cluster_file, center_file, output_file, separator):
    # Convert the input file (cluster_file and center_file) to the format of ITR input
    # the seperator is the seperator used in the cluster_file to seperate the clusters
    
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

    def output_for_syntax_ITR(clusters, centers, output_file):
        # Write the clusters and centers to the output file
        with open(output_file, "w") as f:
            for center, cluster in zip(centers, clusters):
                f.write(center + "\n")
                f.write("*****************************\n")
                for element in cluster:
                    f.write(element + "\n")
                f.write("\n\n")

    clusters, centers = input_file(cluster_file, center_file, separator)
    output_for_syntax_ITR(clusters, centers, output_file)



def convert_ITR_output(output_dir):
    # Convert the ITR output to the format of the other tools
    # the output_dir should contain the output-results-success.txt and output-results-fail.txt files
    
    adjusted_output_file = pathlib.Path(output_dir) / "itr_output.txt"

    current_cluster_id = 0
    current_output = ""
    output_dict = {}
    line_index = 0
    
    with open(pathlib.Path(output_dir) / "output-results-success.txt", "r") as f:
        for line in f.readlines():
            if line_index % 5 == 0:
                current_cluster_id = int(line.split(" ")[-1])
            
            # the next line would be the output
            elif line_index % 5 == 1:
                current_output = line.strip()
                output_dict[current_cluster_id] = current_output
            
            line_index += 1

    line_index = 0
    
    with open(pathlib.Path(output_dir) / "output-results-fail.txt", "r") as f:
        for line in f.readlines():
            if line_index % 5 == 0:
                current_cluster_id = int(line.split(" ")[-1])
            
            # the next line would be the output
            elif line_index % 5 == 2:
                current_output = line.strip()
                output_dict[current_cluster_id] = current_output
            
            line_index += 1

    with open(adjusted_output_file, "w") as f:
        for i in range(len(output_dict)):
            f.write(output_dict[i+1] + "\n")



def benchmark_all(center_file, cluster_file, read_length, seperator, output_dir, subs_rate = 0.03, del_rate = 0.02, ins_rate = 0.02):
    subprocess.run(["mkdir", "-p", output_dir])

    # also create a log directory under output_dir, use pathlib.Path
    log_dir = pathlib.Path(output_dir) / "logs"
    subprocess.run(["mkdir", "-p", log_dir])

    # Run BBS
    bbs_output_file = pathlib.Path(output_dir) / "bbs_output.txt"
    bbs_time_report_file = pathlib.Path(log_dir) / "bbs_time_report.txt"
    #print("BBS output file: ", bbs_output_file)

    with open(bbs_output_file, "w") as f:
        subprocess.run(["/usr/bin/time", "-o", str(bbs_time_report_file), "-v", 
                        "./bbs", "-i", cluster_file, 
                                 "-l", str(read_length),
                                 "-s", seperator], stdout=f)


    # Run Muscle
    muscle_output_file = pathlib.Path(output_dir) / "muscle_output.txt"
    muscle_time_report_file = pathlib.Path(log_dir) / "muscle_time_report.txt"
    #print("Muscle output file: ", muscle_output_file)   

    subprocess.run(["/usr/bin/time", "-o", str(muscle_time_report_file), "-v", 
                    "python", "./run_muscle.py", "-i", cluster_file,
                                                 "-c", center_file, 
                                                 "-o", muscle_output_file, 
                                                 "-s", seperator])

    # Remove the temporary files
    subprocess.run(["rm", "clm.fasta"])
    subprocess.run(["rm", "clmout.fasta"])


    # Run Trellis BMA
    trellis_bma_file = pathlib.Path(output_dir) / "trellis_bma_output.txt"
    trellis_bma_time_report_file = pathlib.Path(log_dir) / "trellis_bma_time_report.txt"


    subprocess.run(["/usr/bin/time", "-o", str(trellis_bma_time_report_file), "-v", 
                    "python", "./run_trellis_bma.py", "-i", cluster_file, 
                                                      "-c", center_file, 
                                                      "-l", str(read_length), 
                                                      "-o", trellis_bma_file, 
                                                      "-s", seperator, 
                                                      "-b", str(subs_rate), 
                                                      "-d", str(del_rate), 
                                                      "-n", str(ins_rate)], stderr=subprocess.DEVNULL)

    # Run ITR
    # Convert the input file to the format of ITR input
    itr_input_file = pathlib.Path(output_dir) / "itr_input.txt"
    itr_output_file = pathlib.Path(output_dir) /  "itr_direct_output.txt"
    itr_time_report_file = pathlib.Path(log_dir) / "itr_time_report.txt"
    convert_ITR_input(cluster_file, center_file, itr_input_file, seperator)

    
    subprocess.run(["/usr/bin/time", "-o", str(itr_time_report_file), "-v",
                    "python", "./run_ITR.py", "-i", itr_input_file,
                                              "-d", output_dir, 
                                              "-o", itr_output_file])
    
    # Convert the ITR output to the format of the other tools
    convert_ITR_output(output_dir)

    subprocess.run(["rm", itr_input_file])


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run all tools")
    parser.add_argument("-i", "--input", required=True, help="Path to the cluster file.")
    parser.add_argument("-c", "--center", required=True, help="Path to the center file.")
    parser.add_argument("-l", "--read-length", required=True, help="Length of the reads.")
    parser.add_argument("-o", "--output", required=True, help="Path to the output directory.")
    parser.add_argument("-s", "--separator", default="===", help="Separator used in the cluster file.")
    parser.add_argument("-b", "--substitution-rate", required=True, help="Substitution rate.")
    parser.add_argument("-d", "--deletion-rate", required=True, help="Deletion rate.")
    parser.add_argument("-n", "--insertion-rate", required=True, help="Insertion rate.")

    args = parser.parse_args()

    benchmark_all(args.center, args.input, int(args.read_length), args.separator, args.output, float(args.substitution_rate), float(args.deletion_rate), float(args.insertion_rate))

