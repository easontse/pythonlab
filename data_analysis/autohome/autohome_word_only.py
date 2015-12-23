import csv

input_file = open('autohome_with_adj_n.csv')
output_file = open('autohome_word_only.txt', 'w')
csv_reader = csv.reader(input_file)

for row in csv_reader:
        output_file.write(row[5] + '\n')