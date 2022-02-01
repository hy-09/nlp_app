from api.util.aozora import *
import random
from janome.tokenizer import Tokenizer

tokenizer = Tokenizer()

def get_synthesized_content_title(urls, titles):
    content = get_synthesized_content(urls)
    title = get_synthesized_title(titles)

    return content, title

def get_synthesized_content(urls):
    flat_text = get_all_flat_text_from_zip_list(urls)
    markov_dict = make_markov_dict(flat_text, 3)

    line_count = 13
    lines = []
    for a in range(line_count):
        lines.append(make_markov_sentence(markov_dict)[7:-7])
        print(make_markov_sentence(markov_dict))

    return '\n'.join(lines)

def make_wakati_list(input_str):
    result_list = []
    tokens = tokenizer.tokenize(input_str)
    for token in tokens:
        # 元の単語＋半角スペースを追加しているため、
        # 結果とした、単語の切れ目全てに半角スペースが入る
        result_list.append(token.surface)
    return result_list

def make_markov_dict(text, chain_number):
    # マルコフ連鎖用の辞書
    markov_dict = {}
    text_lines = text.split('\n')

    # １行ごとに処理してマルコフ連鎖用の辞書に追記していく
    for one_line in text_lines:
        # １行ごとに、改行コードやタブなどを消す（綺麗化前処理）
        one_line = ''.join(one_line.splitlines())
        # 形態素解析して、１行を、単語リストにする
        word_list = make_wakati_list(one_line)

        # 単語リストの最初と最後に、文頭/文末を示すフラグを追加する
        word_list = ["__BOS__"] +  word_list + ["__EOS__"]

        # 最低でもchain_number+1個の単語が残っている必要があり、
        # word_listの単語数が十分な間は処理を繰り返す
        while len(word_list) > chain_number:
            # 最初の chain_number 個の単語を、辞書に登録する際のキーとする。
            # （辞書のキーとして扱うため、tupleという形式に変換しておく）
            # key = ("__BOF__", "この", "文章") value = "を" のような形で格納される。
            # ループの２回目では、最初の"__BOF__"が削除されて繰り返されるため、
            # key = ("この", "文章", "を") value = "単語" のような形になる。以下同様  
            key = tuple( word_list[0 : chain_number] )
            # 次に続く単語は、そのキーの次の単語
            value = word_list[chain_number]
            markov_dict

            # 初回登録の場合、そのkeyに対する空のリストを作る処理
            # 既にそのkeyに対するデータがある場合は何もしない
            markov_dict.setdefault(key, [] )

            # そのkeyに登録されているリストに、今回のvalueを追加する
            markov_dict[key].append(value)

            # リストの最初の単語を削除する
            # ※ここでだんだん単語数が減っていくため、いつかはループ処理を抜ける
            word_list.pop(0)
    
    # 全ての行を処理し終わったら、完成した辞書データをリターン
    return markov_dict

# マルコフ連鎖用の辞書と最初のキー候補リストを入れると文章を作る関数
def make_markov_sentence(markov_dict):
    # 出力用の文字列
    output_sentence = ""

    # 最大１万回ランダムに繰り返して冒頭を取得する
    key_list = list(markov_dict.keys())
    for a in range(10000):
        # 最初のキーをランダムに取得する
        key = random.choice(key_list)
        # 文頭のフラグが出るまで繰り返し
        if key[0] == "__BOS__":
            break
    
    # key(tuple型)を結合して文字列にして追記
    output_sentence += "".join(map(str, key))
    
    # 最大１万回繰り返し（通常は途中でbreakして終了）
    for a in range(10000):
        # keyに対応するvalue（次の単語候補のリスト）を取得
        value = markov_dict.get(key)
        # 例外処理：もしkeyが辞書に見つからない場合処理終了
        if value == None:
            break

        # 単語のリストから次の単語をランダムに選ぶ
        next_word = random.choice(value)
        # 文章に追記する
        output_sentence += next_word
        # 文末のフラグが出ていたら終了
        if next_word == "__EOS__":
            break
        
        # 既存キーの最初を除外して、next_wordをくっつけて新しいkeyに更新する
        # ※tupleの結合処理
        key = key[1:] + (next_word, )
    
    # 生成された文章を返す
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
            print(word_count)
            return ''.join(random.sample(dict['名詞'], word_count))
    else:
        return 'ツァラトゥストラはかく語りき'

    