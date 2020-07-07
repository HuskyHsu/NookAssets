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

def getLanguage(sheet):
    language = ['id', 'Chinese (Traditional)', 'English', 'Japanese']

    data = list(map(lambda field: sheet[field].tolist(), language))
    idMap = {}
    for index, id in enumerate(data[0]):
        idMap[id] = {'zh-tw': data[1][index], 'en-us': data[2][index], 'ja-jp': data[3][index]}
    
    return idMap

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