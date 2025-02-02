lines_seen = set() # holds lines already seen
outfile = open("../../../home-18TB/puru/ClusteringData_baseline/EncodedStrands_woDupes.txt", "w")
for line in open("../../../home-18TB/puru/ClusteringData_baseline/EncodedStrands.txt", "r"):
    if line not in lines_seen: # not a duplicate
        outfile.write(line)
        lines_seen.add(line)
outfile.close()