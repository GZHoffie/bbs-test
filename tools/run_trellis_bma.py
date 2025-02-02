import sys

sys.path.append('/home/zhenhao/bbs-test/tools/TrellisBMA/')

from trellis_bma import *
from helper_functions import *
import pandas as pd
import numpy as np
from scipy.stats import mode

from conv_code import *
from coded_ids_multiD import *
from bma import *

import seaborn as sns

def read_files_trellis_bma(cluster_file, center_file, seperator = "==="):
    centers_list_chars = []
    centers_str = []
    with open(center_file) as f:
        for l in f:
            centers_list_chars.append(list(l.split()[0]))
            centers_str.append(l.split()[0])
    centers_list_chars = np.array(centers_list_chars)

    traces_list_chars = []
    traces_str = []
    with open(cluster_file) as f:
        for l in f:
            if seperator in l:
                traces_list_chars.append([])
                traces_str.append([])
            else:
                traces_list_chars[-1].append(np.array(list(l.split()[0])))
                traces_str[-1].append(l.split()[0])

    def map2int(strarray, chars):
        maps = {}
        for i in range(len(chars)):
            maps[chars[i]] = i
        intarray = np.zeros_like(strarray, dtype = int)
        for i in range(len(strarray)):
            intarray[i] = maps[strarray[i]]
        return intarray


    alphabet = ['A','C','G','T']
    centers_list = []
    traces_list = []
    for i in trange(len(centers_list_chars), desc = "Creating dataset"):
        centers_list.append(map2int(centers_list_chars[i], alphabet))
        traces_list.append([])
        for j in range(len(traces_list_chars[i])):
            traces_list[-1].append(map2int(traces_list_chars[i][j], alphabet))

    return centers_list, traces_list


def int_array_to_str(int_array):
    alphabet = ['A','C','G','T']
    return ''.join([alphabet[i] for i in int_array])

def process_cluster(ids_trellis, traces, cc, index):
    Tbma_LA_estimate = trellis_bma(ids_trellis, traces, cc.trellis_states[0][0],\
                                        cc.trellis_states[-1], lookahead=True)[0]
    return index, int_array_to_str(Tbma_LA_estimate)


def run_trellis_bma(cluster_file, center_file, read_length, output_file, seperator = "===", subs_rate = 0.03, del_rate = 0.02, ins_rate = 0.02, multithreaded = False):
    in_len = read_length
    N_cw = read_length
    redundancy = N_cw-in_len

    A_in = 4
    A_cw = 4

    cc = conv_code()
    G = np.array([[1]])
    cc.quar_cc(G)
    cc.make_trellis(in_len)
    cc.make_encoder()
    code_trellis_states = cc.trellis_states
    code_trellis_edges = cc.trellis_edges
    code_time_type = cc.time_type


    num_traces = 1
    p_del = del_rate
    p_sub = subs_rate
    p_ins = ins_rate
    max_drift = 15

    ids_trellis = coded_ids_multiD(A_in, A_cw, code_trellis_states,code_trellis_edges, code_time_type,\
                    num_traces, p_del, p_sub, p_ins, max_drift, input_prior = None)
    
    # read in the data
    centers_list, traces_list = read_files_trellis_bma(cluster_file, center_file, seperator)
    #print(centers_list[0], traces_list[0])
    results = []


    if not multithreaded:
        with open(output_file, "w") as f:
            for i in range(len(traces_list)):
                if i % 100 == 0:
                    print("%",round(i*100/len(traces_list),2),"of the clusters are aligned.")
                Tbma_LA_estimate = trellis_bma(ids_trellis, traces_list[i], cc.trellis_states[0][0],\
                                                cc.trellis_states[-1],lookahead = True)[0]
                #results.append(int_array_to_str(Tbma_LA_estimate))
                f.write(int_array_to_str(Tbma_LA_estimate) + "\n")
    else:
        import concurrent.futures

        results_dict = {}

        with concurrent.futures.ProcessPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(process_cluster, ids_trellis, traces_list[i], cc, i) for i in range(len(traces_list))]
            for future in concurrent.futures.as_completed(futures):
                i, result = future.result()
                results_dict[i] = result

        with open(output_file, "w") as f:
            for i in range(len(traces_list)):
                f.write(results_dict[i] + "\n")

    #return results


if __name__ == "__main__":
    import sys

    import argparse
    import multiprocessing

    parser = argparse.ArgumentParser(description="Run MUSCLE alignment on clusters.")
    parser.add_argument("-i", "--input", required=True, help="Path to the cluster file.")
    parser.add_argument("-c", "--center", required=True, help="Path to the center file.")
    parser.add_argument("-o", "--output", required=True, help="Path to the output file.")
    parser.add_argument("-s", "--separator", default="===", help="Separator used in the cluster file.")
    parser.add_argument("-l", "--read-length", required=True, help="Length of the reads.")
    parser.add_argument("-b", "--substitution-rate", required=True, help="Substitution rate.")
    parser.add_argument("-d", "--deletion-rate", required=True, help="Deletion rate.")
    parser.add_argument("-n", "--insertion-rate", required=True, help="Insertion rate.")

    parser.add_argument("-m", "--multithreaded", action="store_true", help="Run in multithreaded mode.")

    args = parser.parse_args()


    print("Running Trellis BMA")

    run_trellis_bma(args.input, args.center, int(args.read_length), args.output, args.separator, float(args.substitution_rate), float(args.deletion_rate), float(args.insertion_rate), args.multithreaded)