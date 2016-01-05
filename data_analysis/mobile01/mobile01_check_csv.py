#!/usr/bin/env python3
import csv
from tqdm import tqdm
with open('mobile01-luxgen_uniq.csv','r') as csvfile:
    reader = csv.reader(csvfile)
    for i in tqdm(reader,mininterval=1,total=229800):
        with open('mobile01-luxgen_uniq_corrected.csv', 'w') as outp:
            writer = csv.writer(outp)
            for i in reader:
                if len(i) == 5:
                    writer.writerow(i)
