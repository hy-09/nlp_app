
import re
import zipfile
import urllib.request
import os.path,glob

def get_flat_text_from_aozora(id, url):
    info = get_book_path_info(id)
    
    book_path = info['book_path']
    contentfile_path = info['contentfile_path']
    
    if not os.path.exists(contentfile_path):
        zip_file_name = re.split(r'/', url)[-1]
        
        if not os.path.exists(zip_file_name):
            data = urllib.request.urlopen(url).read()
            with open(zip_file_name, mode="wb") as f:
                f.write(data)
        
        os.makedirs(book_path)
        
        with zipfile.ZipFile(zip_file_name, 'r') as unzipped_data:
            unzipped_data.extractall(book_path)
        
        os.remove(zip_file_name)

        wild_path = os.path.join(book_path,'*.txt')
        originname_path = glob.glob(wild_path)[0]

        os.rename(originname_path, contentfile_path)
        
    binary_data = open(contentfile_path, 'rb').read()
    main_text = binary_data.decode('shift_jis')

    return main_text


import re

with open('jisx0213-2004-std.txt') as f:
  ms = (re.match(r'(\d-\w{4})\s+U\+(\w{4,5})', l) for l in f if l[0] != '#')
  gaiji_table = {m[1]: chr(int(m[2], 16)) for m in ms if m}

def get_gaiji(s):
  m = re.search(r'第(\d)水準\d-(\d{1,2})-(\d{1,2})', s)
  if m:
    key = f'{m[1]}-{int(m[2])+32:2X}{int(m[3])+32:2X}'
    return gaiji_table.get(key, s)
  m = re.search(r'U\+(\w{4})', s)
  if m:
    return chr(int(m[1], 16))
  m = re.search(r'.*?(\d)-(\d{1,2})-(\d{1,2})', s)
  if m:
    key = f'{int(m[1])+2}-{int(m[2])+32:2X}{int(m[3])+32:2X}'
    return gaiji_table.get(key, s)
  return s

def flatten_aozora(text):
  text = re.sub(r'※［＃.+?］', lambda m: get_gaiji(m[0]), text)
  text = re.split(r'\-{5,}', text)[2]
  text = re.split(r'底本：', text)[0]
  text = re.sub(r'《.+?》', '', text)
  text = re.sub(r'［＃.+?］', '', text)
  text = text.strip()
  return text


import time

def get_all_flat_text_from_zip_list(books):
  all_flat_text = ""
  for book in books: 
    try:
      aozora_dl_text = get_flat_text_from_aozora(book['id'], book['url'])
      flat_text = flatten_aozora(aozora_dl_text) 
      all_flat_text += flat_text + ("\n")
    except:
      import traceback
      traceback.print_exc()
    
    time.sleep(1)
  
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