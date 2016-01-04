#!/usr/bin/env python3.4

import json, csv
import gensim

model = gensim.models.Word2Vec.load_word2vec_format('mobile01-luxgen-2013-15.vector',binary=False)
autohome_count = csv.reader(open('mobile01-luxgen-2013-15_count.csv', 'r'))

target_words = ['車','人','U6','問題','價格','油耗']

related_words = []
for i in target_words:  
    related_words.append([x for x,_ in model.most_similar(i)[0:5]])

related_words_unpack = []
for i in related_words:
    for x in i:
        related_words_unpack.append(x)

count_dict = {row[0]:int(row[1]) for row in autohome_count if row[0] in related_words_unpack}

dataset = {
    'name': 'mobile01-luxgen',
    'children':[
        {
            'name':x,
            'children': [
                {
                    'name': y,
                    'size': count_dict[y]
                } for y,_ in model.most_similar(x)[0:5]
            ]
        } for x in target_words
    ] 
}

print(json.dumps(dataset, indent=2, ensure_ascii=False))
    
with open('mobile01-luxgen-2013-15_linked_data.json','w') as outfile:
    outfile.write(json.dumps(dataset, outfile, indent=2, ensure_ascii=False))