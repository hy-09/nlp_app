# 青空文庫からのダウンロードzip展開＆テキスト抽出

import re
import zipfile
import urllib.request
import os.path,glob

# 青空文庫のURLから小説テキストデータを得る関数
def get_flat_text_from_aozora(id, url):
    info = get_book_path_info(id)
    
    book_path = info['book_path']
    contentfile_path = info['contentfile_path']
    
    if not os.path.exists(contentfile_path):
        # zipファイル名の取得
        zip_file_name = re.split(r'/', url)[-1]
        
        # 既にダウンロード済みか確認後、URLからファイルを取得
        if not os.path.exists(zip_file_name):
            data = urllib.request.urlopen(url).read()
            with open(zip_file_name, mode="wb") as f:
                f.write(data)
        
        # 展開用フォルダを作成
        os.makedirs(book_path)
        
        # zipファイルの中身を全て、展開用フォルダに展開
        with zipfile.ZipFile(zip_file_name, 'r') as unzipped_data:
            unzipped_data.extractall(book_path)
        
        # zipファイルの削除
        os.remove(zip_file_name)
        # 注：展開フォルダの削除は入れていない
        
        # テキストファイル(.txt)の抽出
        wild_path = os.path.join(book_path,'*.txt')
        # テキストファイルは原則1つ同梱。最初の1つを取得
        originname_path = glob.glob(wild_path)[0]

        os.rename(originname_path, contentfile_path)
        
    # 青空文庫はshift_jisのためデコードしてutf8にする
    binary_data = open(contentfile_path, 'rb').read()
    main_text = binary_data.decode('shift_jis')

    # 取得したutf8のテキストデータを返す
    return main_text


# 青空文庫のデータを加工して扱いやすくするコード

import re

# 外字変換のための対応表（jisx0213対応表）の読み込み
with open('jisx0213-2004-std.txt') as f:
  #ms = (re.match(r'(\d-\w{4})\s+U\+(\w{4})', l) for l in f if l[0] != '#')
  # 追加：jisx0213-2004-std.txtには5桁のUnicodeもあるため対応
  ms = (re.match(r'(\d-\w{4})\s+U\+(\w{4,5})', l) for l in f if l[0] != '#')
  gaiji_table = {m[1]: chr(int(m[2], 16)) for m in ms if m}

# 外字データの置き換えのための関数
def get_gaiji(s):
  # ※［＃「弓＋椁のつくり」、第3水準1-84-22］の形式を変換
  m = re.search(r'第(\d)水準\d-(\d{1,2})-(\d{1,2})', s)
  if m:
    key = f'{m[1]}-{int(m[2])+32:2X}{int(m[3])+32:2X}'
    return gaiji_table.get(key, s)
  # ※［＃「身＋單」、U+8EC3、56-1］の形式を変換
  m = re.search(r'U\+(\w{4})', s)
  if m:
    return chr(int(m[1], 16))
  # ※［＃二の字点、1-2-22］、［＃感嘆符二つ、1-8-75］の形式を変換
  m = re.search(r'.*?(\d)-(\d{1,2})-(\d{1,2})', s)
  if m:
    key = f'{int(m[1])+2}-{int(m[2])+32:2X}{int(m[3])+32:2X}'
    return gaiji_table.get(key, s)
  # 不明な形式の場合、元の文字列をそのまま返す
  return s

# 青空文庫の外字データ置き換え＆注釈＆ルビ除去などを行う加工関数
def flatten_aozora(text):
  # textの外字データ表記を漢字に置き換える処理
  text = re.sub(r'※［＃.+?］', lambda m: get_gaiji(m[0]), text)
  # 注釈文や、ルビなどの除去
  text = re.split(r'\-{5,}', text)[2]
  text = re.split(r'底本：', text)[0]
  text = re.sub(r'《.+?》', '', text)
  text = re.sub(r'［＃.+?］', '', text)
  text = text.strip()
  return text


# 複数ファイルのダウンロードや加工を一括実行する関数

import time
# ZIP-URLのリストから全てのデータをダウンロード＆加工する関数
def get_all_flat_text_from_zip_list(books):
  all_flat_text = ""
  for book in books: 
    # ダウンロードや解凍の失敗があり得るためTry文を使う
    # 十分なデータ量があるため数件の失敗はスキップでよい
    try:
      # 青空文庫からダウンロードする関数を実行
      aozora_dl_text = get_flat_text_from_aozora(book['id'], book['url'])
      # 青空文庫のテキストを加工する関数を実行
      flat_text = flatten_aozora(aozora_dl_text) 
      # 結果を追記して改行。
      all_flat_text += flat_text + ("\n")
    except:
      # エラー時の詳細ログが出るおまじない
      import traceback
      traceback.print_exc()
    
    # 青空文庫サーバに負荷をかけすぎないように１秒待ってから次の小説へ
    time.sleep(1)
  
  # 全部がつながった大きなテキストデータを返す
  return all_flat_text

def get_book_path_info(id):
    books_path = 'books/'
    book_path = books_path + str(id) + '/'
    contentfile_name = 'content.txt'
    chartfile_name = 'chart.json'

    return {
        'books_path': books_path,
        'book_path': book_path,
        'contentfile_name': contentfile_name,
        'chartfile_name': chartfile_name,
        'contentfile_path': book_path + contentfile_name,
        'chartfile_path': book_path + chartfile_name,
    }