if __name__ == "__main__":
    import sys
    import subprocess
    import argparse

    parser = argparse.ArgumentParser(description="Run ITR")
    parser.add_argument("-i", "--input_file", type=str, required=True, help="Path to the input file")
    parser.add_argument("-d", "--output_directory", type=str, required=True, help="Path to the output directory")
    parser.add_argument("-o", "--output_file", type=str, required=True, help="Path to the output file")
    args = parser.parse_args()

    print("Running ITR")

    ITR_binary = "/home/zhenhao/bbs-test/tools/Reconstruction/Iterative/DNA"
    with open(args.output_file, "w") as f:
        #print([ITR_binary, args.input_file, args.output_directory])
        subprocess.run([ITR_binary, args.input_file, args.output_directory], stdout=f)