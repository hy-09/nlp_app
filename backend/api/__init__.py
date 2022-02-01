
import csv


np_dic = {}
# utf-8の文字コードを指定してファイルを開く
fp = open("pn.csv", "rt", encoding="utf-8")
# タブ区切り形式でCSVデータを読む
reader = csv.reader(fp, delimiter='\t')
# 各行ごとに処理を行う
for i, row in enumerate(reader):
    # 行ごとのデータは以下の形式であり、
    # 愛情	p	〜がある・高まる（存在・性質）
    # 冒頭の見出し語を name に、
    # 次の p or n or e などを result に格納 
    name = row[0]
    result = row[1]
    np_dic[name] = result
