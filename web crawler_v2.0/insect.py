import math

import parse

if __name__ == '__main__':

    feild = 'Insects'
    outputName = 'insects'

    weather = {
        'Any except rain': '非雨雪天',
        'Any weather': '無影響',
        'Rain only': '雨天',
    }

    where = {
        "Flying near flowers": "飛行(花朵附近)",
        "On rotten turnips": "爛大頭菜上",
        "On trees (any kind)": "樹上(任何種類)",
        "Shaking trees (hardwood or cedar only)": "搖樹(僅闊葉樹/針葉樹)",
        "Flying near water": "飛行(水附近)",
        "On the ground": "地上",
        "On palm trees": "椰子樹上",
        "On hardwood/cedar trees": "闊葉樹/針葉樹上",
        "From hitting rocks": "敲石頭",
        "On tree stumps": "樹樁上",
        "Flying": "飛行",
        "On rivers/ponds": "河流/池塘上",
        "Pushing snowballs": "推雪球",
        "On villagers": "村民身上",
        "Flying near trash (boots, tires, cans) or rotten turnips": "飛行(在垃圾[靴子,輪胎,罐頭]或腐爛的大頭菜附近)",
        "Disguised on shoreline": "偽裝在海岸線上",
        "On flowers": "花上",
        "Underground (dig where noise is loudest)": "地下(挖掘噪音最大的地方)",
        "Flying near light sources": "飛行(光源附近)",
        "On white flowers": "白花上",
        "Flying near blue/purple/black flowers": "飛行(藍色/紫色/黑色花朵附近)",
        "On rocks/bushes": "岩石/灌木叢上",
        "Disguised under trees": "喬裝在樹下",
        "Shaking trees": "搖樹",
        "On beach rocks": "沙灘上"
    }

    translations = parse.readExcel('./rawData/Translations - 1.3.0.xlsx')
    nameMap = parse.getLanguage(translations['Bugs'])
    # print(diveFishName)

    rawData = parse.readExcel("./rawData/Editors' Copy - Data Spreadsheet for ACNH (22).xlsx")
    rawData = rawData[feild]
    
    output = []
    column = [i for i in rawData]
    print(column)
    for index, row in rawData.iterrows():
        pickData = {'type': outputName}

        idName = "Insect_{}".format(str(row['Internal ID']).zfill(5))
        # diveFishName[idName]['zh-tw']

        pickData['id'] = int(row['#'])
        pickData['name_c'] = nameMap[idName]['zh-tw']
        pickData['name_j'] = nameMap[idName]['ja-jp']
        pickData['name_e'] = nameMap[idName]['en-us']

        pickData['Sell'] = int(row['Sell'])
        pickData['Where/How'] = where[row['Where/How']]
        pickData['Weather'] = weather[row['Weather']]
        pickData['Total Catches to Unlock'] = int(row['Total Catches to Unlock'])
        pickData['Spawn Rates'] = row['Spawn Rates']

        N_month = ['NH Jan', 'NH Feb', 'NH Mar', 'NH Apr', 'NH May', 'NH Jun', 'NH Jul', 'NH Aug', 'NH Sep', 'NH Oct', 'NH Nov', 'NH Dec']
        S_month = ['SH Jan', 'SH Feb', 'SH Mar', 'SH Apr', 'SH May', 'SH Jun', 'SH Jul', 'SH Aug', 'SH Sep', 'SH Oct', 'SH Nov', 'SH Dec']
        pickData['N_month'] = [None]*12
        pickData['S_month'] = [None]*12

        for index, m in enumerate(N_month):
            if row[m] == 'All day':
                pickData['N_month'][index] = '全天'
            elif type(row[m]) is str:
                pickData['N_month'][index] = "".join(row[m].split())

        for index, m in enumerate(S_month):
            if row[m] == 'All day':
                pickData['S_month'][index] = '全天'
            elif type(row[m]) is str:
                pickData['S_month'][index] = "".join(row[m].split())

        pickData['filename'] = row['Icon Filename']
        output.append(pickData)

    output = sorted(output, key=lambda k: k['id'])

    parse.saveFile(outputName, output)