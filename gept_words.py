# 台灣測驗中心－全民英檢參考字表
import webutils
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import json
import csv

# 設定 26 個英文字母
list_alphabet = [chr(a) for a in range(65, 91)]
alphabet = ''.join(list_alphabet)
print('alphabet:', alphabet)

# 設定單字級別
word_levels = ('w1', 'w2', 'w3')
vocab_words = [[], [], []]

# 設定 HTTP headers
url = 'http://www.taiwantestcentral.com/WordList/WordListByName.aspx?MainCategoryID=4&Letter={}'
headers = webutils.headers

# 依字母擷取單字表
for aindex, aletter in enumerate(alphabet):
    req = Request(url.format(aletter), headers=headers)
    html = urlopen(req)
    bs_vocab = BeautifulSoup(html.read(), 'html.parser')

    print(f'{aletter}...')
    for windex, wlevel in enumerate(word_levels):
        # 新增 dict
        vocab_words[windex].append({'letter':aletter, 'words':[]})
        # 擷取單字
        list_word = bs_vocab.find_all('td', {'class':wlevel})
        for word in list_word:
            chinese_meaning = word.parent.find('td', {'class':'Chinese'})
            vocab_words[windex][aindex]['words'].append((wlevel, word.get_text(), 
                chinese_meaning.get_text()))

# 設定儲存檔名
json_file = 'gept/gept-word.json'
csv_file  = 'gept/gept-word.csv'

# 寫入 vocab-word.json
print(json.dumps(vocab_words, sort_keys=True, indent=4), file=open(json_file, 'wt'))

# 寫入 vocab-word.csv
word_count = 0
with open(csv_file, 'w', newline='', encoding='utf8') as vocab_words_csv:
    csvwriter = csv.writer(vocab_words_csv)
    for wlevel_words in vocab_words:
        for aletter_words in wlevel_words:
            for word in aletter_words['words']:
                # print(word)
                word_count += 1
                csvwriter.writerow(word)
print('Total:', word_count)
print(json_file)
print(csv_file)
    