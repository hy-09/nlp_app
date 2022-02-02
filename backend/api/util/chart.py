
from api import np_dic
from api.util.aozora import *
from janome.tokenizer import Tokenizer
import json

tokenizer = Tokenizer()


def get_content_chart(id, url):
    info = get_book_path_info(id)

    book_path = info['book_path']
    chartfile_path = info['chartfile_path']

    aozora_dl_text = get_flat_text_from_aozora(id, url)
    flat_text = flatten_aozora(aozora_dl_text) 

    if not os.path.exists(chartfile_path):
        text_list = flat_text.split('\n')

        x =  []
        y1 = []
        y2 = []

        total_word_count = 0
        for text_str in text_list:
            pos_count, neg_count, word_count = np_rate(text_str)

            if word_count <1 :
                continue

            y1.append(pos_count/word_count)
            y2.append(neg_count/word_count)
            total_word_count += word_count
            x.append(total_word_count)

        chart = { "x": x, "pos": y1, "neg": y2}
        
        with open(chartfile_path, 'w') as f:
            json.dump(chart, f)

    else:
        with open(chartfile_path) as f:
            chart = json.load(f)

    return flat_text, chart

def np_rate(input_str):
    pos_count  = 0
    neg_count  = 0
    word_count = 0
    tokens = tokenizer.tokenize(input_str)
    for token in tokens:
        base_form = token.base_form

        if base_form in np_dic:
            if np_dic[base_form] == "p" :
                pos_count += 1
            if np_dic[base_form] == "n" :
                neg_count += 1
                
        word_count += 1
        
    return pos_count, neg_count, word_count