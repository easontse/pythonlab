#!/usr/bin/env python3
import csv
from tqdm import tqdm

input_file = open('mobile01-luxgen-2013-15_with_adj_n.csv')
output_file = open('mobile01-luxgen-2013-15_word_only.txt', 'w')
csv_reader = csv.reader(input_file)

for row in tqdm(csv_reader):
        output_file.write(row[5] + '\n')