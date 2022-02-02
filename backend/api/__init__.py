
import csv


np_dic = {}
fp = open("pn.csv", "rt", encoding="utf-8")
reader = csv.reader(fp, delimiter='\t')

for i, row in enumerate(reader):
    name = row[0]
    result = row[1]
    np_dic[name] = result
