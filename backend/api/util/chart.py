
from api import np_dic
from api.util.aozora import *
from janome.tokenizer import Tokenizer

tokenizer = Tokenizer()


def get_content_chart(url):
    # ダウンロード＆テキスト取得
    aozora_dl_text = get_flat_text_from_aozora(url)

    # タグや外字などのデータを加工
    flat_text = flatten_aozora(aozora_dl_text) 

    # フラットなテキストを「改行コード」で区切ってリスト形式にする
    text_list = flat_text.split('\n')

    # グラフ作成用のx軸,　y軸
    # X座標（物語の進行の時間軸として、それまでの単語総数を入れる）
    x =  []
    # Y座標は２種類＝y1にポジティブ度合い、y2にネガティブ度合いとする
    y1 = []
    y2 = []

    total_word_count = 0
    # 作ったリストの各要素に対して処理を行う
    for text_str in text_list:
        # リストの中身＝文字列に対してネガポジ分析を行う。
        pos_count, neg_count, word_count = np_rate(text_str)
        # 単語数が０となる行があった場合、その行を飛ばす（０除算防止）
        if word_count <1 :
            continue
        # 全単語数に対するポジティブの比率を、リストに追加する
        y1.append(pos_count/word_count)
        # 全単語数に対するポジティブの比率を、リストに追加する
        y2.append(neg_count/word_count)
        # これまでに出てきた単語数の合計をX軸とする
        total_word_count += word_count
        x.append(total_word_count)

    return flat_text, { 'x': x, 'pos': y1, 'neg': y2}

def np_rate(input_str):
    pos_count  = 0
    neg_count  = 0
    word_count = 0
    tokens = tokenizer.tokenize(input_str)
    for token in tokens:
        base_form = token.base_form # 原形/基本形
        # ネガポジ辞書に存在するか確認して対応する方を1増やす
        if base_form in np_dic:
            # 単語を辞書のキーとして、そのバリューが p か n か確認する
            if np_dic[base_form] == "p" :
                pos_count += 1
            if np_dic[base_form] == "n" :
                neg_count += 1
        # 存在しようがしまいが、単語数を1増やす
        word_count += 1
        
    return pos_count, neg_count, word_count