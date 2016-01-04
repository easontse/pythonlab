#!/usr/bin/env python3.5
# coding: utf-8

# In[1]:

import csv, psycopg2, jieba, operator, time
jieba.load_userdict('dict.txt.big')
import jieba.posseg as pseg
import pandas as pd
from tqdm import tqdm


jieba.enable_parallel()

def pseg_adj_n(row):
    pair_pseg = [item for item in pseg.lcut(row[3])]

    adj = [[word, flag][0] for word, flag in pair_pseg if flag[0] == 'a']
    n = [[word, flag][0] for word, flag in pair_pseg if flag[0] == 'n']

    dataset = [adj, n]
    return dataset

csv_reader = csv.reader(open('mobile01-luxgen-2013-15.csv'))
nounlist = []
with open('mobile01-luxgen-2013-15_with_adj_n.csv', 'w') as csvfile:
    textwriter = csv.writer(csvfile, delimiter=',')
    for row in tqdm(csv_reader):
        pseg_result = pseg_adj_n(row)
        
        textwriter.writerow([
            row[0],
            row[1],
            row[2],
            row[3],
            ' '.join(pseg_result[0]),
            ' '.join(pseg_result[1]),
            row[4]
        ])
        nounlist.append(pseg_result[1])

nounlist_unpack = []
for i in nounlist:
    for x in i:
        nounlist_unpack.append(x)

noun_series = pd.Series(nounlist_unpack)

with open('mobile01-luxgen-2013-15_count.csv', 'w') as csvfile:
    noun_series.value_counts().to_csv(csvfile)