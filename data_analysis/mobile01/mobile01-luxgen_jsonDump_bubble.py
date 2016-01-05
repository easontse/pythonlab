#!/usr/bin/env python3.4

import json, csv
import gensim

model = gensim.models.Word2Vec.load_word2vec_format('mobile01-luxgen-2013-15_uniq.vector',binary=False)
autohome_count = csv.reader(open('mobile01-luxgen-2013-15_uniq_count.csv', 'r'))

target_words = ['車','人','U6','問題','價格','油耗']

related_words = []
for i in target_words:  
    related_words.append([x for x,_ in model.most_similar(i)[0:5]])

related_words_unpack = []
for i in related_words:
    for x in i:
        related_words_unpack.append(x)

count_dict = {row[0]:int(row[1]) for row in autohome_count if row[0] in related_words_unpack}

with open('mobile01-luxgen-2013-15_uniq_with_adj_n.csv','r') as raw_data:
    csv_reader = csv.reader(raw_data)
    a = []
    for row in csv_reader:
        for word in related_words_unpack:
            if word in row[5] and [word, row[2]] not in a:
                a.append([word, row[2]])

dict_list= {word:[i[1] for i in a if i[0] == word][:5] for word in related_words_unpack}

dataset = []
for i in target_words:
    dataset.append(
        {'name':i,
         'children': [{'topic':x,
                       'rate':count_dict[x], 
                       'link':[
                                {'title':y,'url':'https://www.google.ca/?gws_rd=ssl'} 
                                for y in dict_list[x]
                              ]
                      } for x,_ in model.most_similar(i)[0:5]]
        }
    )

print(json.dumps(dataset, indent=4, ensure_ascii=False))
    
with open('mobile01-luxgen-2013-15_uniq_bubble.json','w') as outfile:
    outfile.write(json.dumps(dataset, outfile, indent=4, ensure_ascii=False))