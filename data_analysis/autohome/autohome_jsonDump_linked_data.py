import json, csv
import gensim

model = gensim.models.Word2Vec.load_word2vec_format('autohome_word_only.vector',binary=False)
autohome_count = csv.reader(open('autohome_count.csv', 'r'))

target_words = ['U6','车','纳智捷','优6','价格','油耗']

related_words = []
for i in target_words:  
    related_words.append([x for x,_ in model.most_similar(i)[0:5]])

related_words_unpack = []
for i in related_words:
    for x in i:
        related_words_unpack.append(x)

count_dict = {row[0]:int(row[1]) for row in autohome_count if row[0] in related_words_unpack}

dataset = {
    'name': 'autohome',
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
    
with open('autohome_linked_data.json','w') as outfile:
    outfile.write(json.dumps(dataset, outfile, indent=2, ensure_ascii=False))