import urllib.request
import json
from docx import Document
from docx.shared import Inches, Pt

word_levels = {'w1':'初級', 'w2':'中級', 'w3':'中高級'}
column_names = ['級別', '單字', '意義']
url = 'http://localhost:5000/vocab_word_json/{}'
filename = 'vocab-word-{}.docx'



for wl in word_levels.keys():
    fho = open("gept/gept-word.json")
    response_data = fho.read()
    json_data = json.loads(response_data)
    fho.close()
    # method: post
    # 設定 data 參數即自動調整為 post
    # req = urllib.request.urlopen(url.format(wl), data={})
    # response_data = req.read()
    # json_data = json.loads(response_data)

    # 設定一般字型
    doc = Document()
    font = doc.styles['Normal'].font
    font.size = Pt(12)

    # 檔案標題
    doc.add_heading('VOCAB 全民英檢字彙表', 0)
    p = doc.add_paragraph()
    p.add_run('General English Proficiency Test Word Lists').italic = True
    doc.add_heading(word_levels[wl]+'字彙', level=1)

    # 表格標題
    table = doc.add_table(rows=1, cols=3, style="Light Grid")
    hdr_cells = table.rows[0].cells
    for i in range(3):
        hdr_cells[i].text = column_names[i]

    # 表格內容
    total = 0
    counter = 0


    for wlevel in json_data:
        # 每個級別新增 100 字彙
        if total == 100:
            break
        # 每個字母新增 10 個字彙
        counter = 0
        for data in wlevel:
            for word in data['words']:
                if counter != 0 and counter % 10 == 0:
                    break
                # 新增單字的長度大於等於 5
                # word[1]：english vocabulary
                # word[2]：chinese vocabulary  
                if len(word[1]) >= 5:
                    total += 1
                    counter += 1
                    word[0] = str(total)
                    print(word)
                    row_cells = table.add_row().cells
                    for i in range(3):
                        row_cells[i].text = word[i]

    doc.save(filename.format(wl))
    