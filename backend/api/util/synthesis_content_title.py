from api.util.aozora import *
import random
from janome.tokenizer import Tokenizer

tokenizer = Tokenizer()

def get_synthesized_content_title(books):
    titles = [book['title'] for book in books]
    
    content = get_synthesized_content(books)
    title = get_synthesized_title(titles)

    return content, title

def get_synthesized_content(books):
    flat_text = get_all_flat_text_from_zip_list(books)
    markov_dict = make_markov_dict(flat_text, 3)

    line_count = 13
    lines = []
    for a in range(line_count):
        lines.append(make_markov_sentence(markov_dict)[7:-7])

    return '\n'.join(lines)

def make_wakati_list(input_str):
    result_list = []
    tokens = tokenizer.tokenize(input_str)
    for token in tokens:
        result_list.append(token.surface)
    return result_list

def make_markov_dict(text, chain_number):
    markov_dict = {}
    text_lines = text.split('\n')

    for one_line in text_lines:
        one_line = ''.join(one_line.splitlines())
        word_list = make_wakati_list(one_line)

        word_list = ["__BOS__"] +  word_list + ["__EOS__"]

        while len(word_list) > chain_number: 
            key = tuple( word_list[0 : chain_number] )
            value = word_list[chain_number]
            markov_dict

            markov_dict.setdefault(key, [] )
            markov_dict[key].append(value)
            word_list.pop(0)
    
    return markov_dict

def make_markov_sentence(markov_dict):
    output_sentence = ""
    key_list = list(markov_dict.keys())

    for a in range(10000):
        key = random.choice(key_list)
        if key[0] == "__BOS__":
            break
    
    output_sentence += "".join(map(str, key))
    
    for a in range(10000):
        value = markov_dict.get(key)
        if value == None:
            break

        next_word = random.choice(value)
        output_sentence += next_word
        if next_word == "__EOS__":
            break
        
        key = key[1:] + (next_word, )
    
    return output_sentence


def get_synthesized_title(titles):
    dict = {}
    for title in titles:
        tokens = tokenizer.tokenize(title)

        for token in tokens:
            pos = token.part_of_speech.split(',')[0]
            if pos not in dict.keys():
                dict[pos] = [token.base_form]
            else:
                dict[pos].append(token.base_form)

    if '名詞' in dict:
        if '助詞' in dict:
            if 'は' in dict['助詞']:
                nouns = random.sample(dict['名詞'], 2)
                return nouns[0] + 'は' + nouns[1]
            elif 'の' in dict['助詞']:
                nouns = random.sample(dict['名詞'], 2)
                return nouns[0] + 'の' + nouns[1]
            else:
                word_count = random.randrange(1, len(dict['名詞'])+1)
                return ''.join(random.sample(dict['名詞'], word_count))
        else:
            word_count = random.randrange(1, len(dict['名詞'])+1)
            return ''.join(random.sample(dict['名詞'], word_count))
    else:
        return 'ツァラトゥストラはかく語りき'

    