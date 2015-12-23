import json, csv
import gensim

model = gensim.models.Word2Vec.load_word2vec_format('autohome_word_only.vector',binary=False)
autohome_count = csv.reader(open('autohome_count.csv', 'r'))

target_words = ['U6','车','纳智捷','优6','上市','感觉']

related_words = []
for i in target_words:  
    related_words.append([x for x,_ in model.most_similar(i)[0:5]])

related_words_unpack = []
for i in related_words:
    for x in i:
        related_words_unpack.append(x)

count_dict = {row[0]:int(row[1]) for row in autohome_count if row[0] in related_words_unpack}

a = []
for i in target_words:
    a.append(
        {'name':i,
         'children': [{'topic':x, 'rate':count_dict[x]} for x,_ in model.most_similar(i)[0:5]]
        }
    )

print(json.dumps(a, indent=4, ensure_ascii=False))
    
with open('autohome.json','w') as outfile:
    json.dumps(a, outfile, indent=4, ensure_ascii=False)