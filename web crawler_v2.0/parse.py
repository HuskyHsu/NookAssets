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

def getRawData():
    return readExcel("./rawData/Data Spreadsheet for Animal Crossing New Horizons.xlsx")

def getCustomLanguageMap():
    df = readExcel('./rawData/Translations - custom.xlsx', 0)

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

def getLanguage(sheet, idField = 'id', lower = ''):
    language = [idField, 'Chinese (Traditional)', 'English', 'Japanese']

    data = list(map(lambda field: sheet[field].tolist(), language))
    idMap = {}
    for index, row in enumerate(data[0]):
        if lower != '':
            row = row.lower()
        idMap[row] = {'zh-tw': data[1][index], 'en-us': data[2][index], 'ja-jp': data[3][index]}

    return idMap

def getLanguageMap(path, onlyId = False):
    m = {}
    with open('../../acnh-message/{}.csv'.format(path), newline='', encoding='utf-8') as csvfile:
        rows = csv.reader(csvfile)
        headers = next(rows)
        if onlyId:
            for row in rows:
                m['_'.join(row[0].split('_')[1:])] = row[1]
        else:
            for row in rows:
                m[row[0]] = row[1]

    return m

def getSeries():
    return {
        "iron": "鑄鐵",
        "ironwood": "鑄鐵木",
        "diner": "餐館",
        "antique": "古董",
        "golden": "黃金",
        "zen": "東方風",
        "shell": "貝殼",
        "mush": "蘑菇",
        "cute": "可愛",
        "bamboo": "竹子",
        "wooden block": "積木",
        "spooky": "萬聖節",
        "fruits": "水果",
        "log": "圓木",
        "wooden": "木製",
        "rattan": "藤編",
        "throwback": "TOY",
        "frozen": "冰塊",
        "stars": "星星",
        "flowers": "花朵",
        "tree's bounty or leaves": "樹果‧落葉",
        "cherry blossoms": "櫻花",
        "cardboard": "紙箱",
        "motherly": "媽媽",
        "festive": "聖誕節",
        "Bunny Day": "復活節",
        "wedding": "婚禮",
        "pirate": "海盜",
        "mermaid": "人魚",
        "None": "無"
    }

def getRecipe(version = '1.5.0'):
    translations = readExcel(f'./rawData/Translations - {version}.xlsx')

    nameSource = ['Craft', 'Plants', 'Tools', 'ETC', 'Event Items', 'Furniture', 'Shells', 'Floors', 'Walls', 'Dresses']
    materialNames = [getLanguage(translations[t], 'English', 'lower') for t in nameSource]

    nameMapCustom = getCustomLanguageMap()

    rawData = getRawData()
    recipeMap = {}
    for index, recipe in rawData['Recipes'].iterrows():
        pickData = {}
        pickData['diyInfoMaterials'] = []

        for i in range(1, 6):
            material = recipe['Material {}'.format(i)]
            if str(material) == 'nan':
                continue

            material = material.lower()
            name = None
            if material == 'fossil':
                name = {'zh-tw': '化石'}
            if material == 'bells':
                name = {'zh-tw': '鈴錢'}

            for materialName in materialNames:
                if material in materialName and name is None:
                    name = materialName[material]

            if name is None:
                print(material)

            pickData['diyInfoMaterials'].append(
                {
                    'count': int(recipe['#{}'.format(i)]),
                    'itemName': name['zh-tw']
                }
            )

        # print(recipe['Source Notes'])
        pickData['diyInfoObtainedFrom'] = [nameMapCustom[s]['zh-tw'] for s in recipe['Source'].split('; ')]
        try:
            pickData['diyInfoSourceNotes'] = nameMapCustom[recipe['Source Notes']]['zh-tw'] if str(recipe['Source Notes']) != 'nan' else None
        except:
            print(recipe['Source Notes'])
            pickData['diyInfoSourceNotes'] = recipe['Source Notes']

        recipeMap[recipe['Crafted Item Internal ID']] = pickData

    return recipeMap

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

    df1 = pd.read_json(json.dumps(output))
    with pd.ExcelWriter('./cleanData/output.xlsx', mode='a', engine="openpyxl") as writer:
        workBook = writer.book
        try:
            workBook.remove(workBook[category])
        except:
            print(f"worksheet[{category}] doesn't exist")
        finally:
            df1.to_excel(writer, sheet_name=category, columns=dictName, index=False)

    print('save {} over'.format(category))