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
        else:
            print(i)
            print('Actual:\t',answer[i])
            print('Recon: \t', reconstructed_strands[i])

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
    


    success_rate = correct / len(answer)
    return hamming_distance, edit_distance, success_rate

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Benchmark the results of a reconstruction algorithm')
    parser.add_argument("-o", "--output_file", type=str, required=True, help="Path to the output file")
    parser.add_argument("-a", "--answer_file", type=str, required=True, help="Path to the answer file")

    args = parser.parse_args()

    hamming_distance, edit_distance, success_rate = benchmark(args.output_file, args.answer_file)

    # print the results
    print("Hamming Distance: ", hamming_distance)
    print("Edit Distance: ", edit_distance)
    print("Success Rate: ", success_rate)
