import random

characters = "ACGT"
print(characters)

strands = []

# 10000000 = 12GB NoisyStrands.txt
length = 1000

for i in range(1000):
    result_strand = ''.join(random.choice(characters) for i in range(length))
    strands.append(result_strand)

f=open(f"./EncodedStrands_{length}.txt", "w")
for s in strands:
    f.write(s+"\n")
f.close()