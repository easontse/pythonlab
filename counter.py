genome = ["A","T","G","C","A","A","T"]
counter = {'A':0,'B':0,'G':0,'C':0}

for gene in genome:
	counter[gene] = counter[gene] + 1

print(counter)