
# coding: utf-8

# In[1]:

import csv, psycopg2, jieba, operator
jieba.load_userdict('autohome_dict.txt')
import jieba.posseg as pseg

jieba.enable_parallel()

def pseg_adj_n(row):
    pair_pseg = [item for item in pseg.lcut(row[3])]
    adj = [[word, flag][0] for word, flag in pair_pseg if flag[0] == 'a']
    n = [[word, flag][0] for word, flag in pair_pseg if flag[0] == 'n']
    dataset = [adj, n]
    return dataset

autohome_csv_reader = csv.reader(open('autohome.csv'))
autohome_new, nounlist = [], []
with open('autohome_with_adj_n.csv', 'w') as csvfile:
    textwriter = csv.writer(csvfile, delimiter=',')
    for row in autohome_csv_reader:
        pseg_result = pseg_adj_n(row)
        
        textwriter.writerow([
            row[0],
            row[1],
            row[2],
            row[3],
            pseg_result[0],
            pseg_result[1]
        ])
        nounlist.append(pseg_result[1])

nounlist_unpack = []
for i in nounlist:
    for x in i:
        nounlist_unpack.append(x)

word_count = {word:nounlist_unpack.count(word) for word in nounlist_unpack}
word_count = sorted(word_count.items(),key=operator.itemgetter(1),reverse=True)

with open('autohome_count.csv', 'w') as csvfile:
    textwriter = csv.writer(csvfile, delimiter=',')
    for word, count in word_count[:30]:
        textwriter.writerow([word, str(count)])
