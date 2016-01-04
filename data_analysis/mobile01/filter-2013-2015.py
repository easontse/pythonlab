#!/usr/bin/env python3

import csv
from tqdm import tqdm

with open('mobile01-luxgen-clone.csv', 'r') as rawdata:
    reader = csv.reader(rawdata)
    tgt_year = ['2015','2014','2013']
    with open('mobile01-luxgen-2013-15.csv','w') as outfile:
        writer = csv.writer(outfile)
        for i in tqdm(reader):
            if i[0][:4] in tgt_year:
                writer.writerow(i)