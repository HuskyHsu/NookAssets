import json
import csv
import pandas as pd

def readExcel(filePath, index = None):
    try:
        df = pd.read_excel(filePath, sheetname=index)
    except:
        df = pd.read_excel(filePath, sheet_name=index)
    
    print('read {} over'.format(filePath.split('/')[-1]))
    return df

def getCustomLanguageMap():
    df = readExcel('../tempData/Furniture.xlsx', 0)

    # EnTwTable = ['類別', '取得方式', '標籤', '主題', '款式', '樣式', '款式說明', '樣式說明', 'DIY相關', '藝術品', '作者/年代/材質', '藝術品真實圖', '村民']
    EnTwTable = ['取得方式', '標籤', '主題', 'DIY相關']

    nameMapCustom = {}
    for EnTw in EnTwTable:
        itemType_en = df[EnTw].tolist()
        itemType_tw = df['{}_tw'.format(EnTw)].tolist()
        itemType_en = [x for x in itemType_en if str(x) != 'nan']
        itemType_tw = [x for x in itemType_tw if str(x) != 'nan']

        for item in zip(itemType_en, itemType_tw):
            if item[0] in nameMapCustom and item[1] != nameMapCustom[item[0]]['zh-tw']:
                print(item)
                print(nameMapCustom[item[0]])
                print('------\n')

            nameMapCustom[item[0]] = {
                'zh-tw': item[1]
            }

    print('Custom {} i18n data'.format(len(nameMapCustom.keys())))
    
    return nameMapCustom

def getLanguage(sheet, idField = 'id'):
    language = [idField, 'Chinese (Traditional)', 'English', 'Japanese']

    data = list(map(lambda field: sheet[field].tolist(), language))
    idMap = {}
    for index, row in enumerate(data[0]):
        idMap[row] = {'zh-tw': data[1][index], 'en-us': data[2][index], 'ja-jp': data[3][index]}
    
    return idMap

def getLanguageMap(path):
    m = {}
    with open('../../acnh-message/{}.csv'.format(path), newline='', encoding='utf-8') as csvfile:
        rows = csv.reader(csvfile)
        headers = next(rows)
        for row in rows:
            m[row[0]] = row[1]

    return m

def saveFile(category, output):

    dictName = output[0].keys()

    with open('../../nook_link/src/data/{}.json'.format(category), 'wt') as fout:
        fout.write(json.dumps(output))

    with open('./cleanData/{}.csv'.format(category), 'wt', encoding='UTF-8', newline='') as fout:
        csvout = csv.writer(fout)

        output_csv = [dictName]
        for row in output:
            row_ = [row[name] for name in dictName]
            output_csv.append(row_)
        csvout.writerows(output_csv)
    
    print('save {} over'.format(category))