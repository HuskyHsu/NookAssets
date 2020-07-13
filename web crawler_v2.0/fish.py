import math

import parse

if __name__ == '__main__':

    feild = 'Fish'
    outputName = 'fish'

    shadow = {
        "X-Small": "極小",
        "Small": "小",
        "Medium": "中",
        "Large": "大",
        "X-Large": "特大",
        "XX-Large": "超特大",
        "Long": "細長",
        "Medium w/Fin": "背鰭(中)",
        "Large w/Fin": "背鰭(大)"
    }

    where = {
        "Sea": "大海",
        "River": "河川",
        "Pier": "碼頭",
        "Pond": "池塘",
        "River (clifftop)": "河(懸崖)",
        "Sea (rainy days)": "大海(雨天)",
        "River (mouth)": "出海口"
    }

    translations = parse.readExcel('./rawData/Translations - 1.3.0.xlsx')
    nameMap = parse.getLanguage(translations[feild])
    # print(diveFishName)

    rawData = parse.readExcel("./rawData/Editors' Copy - Data Spreadsheet for ACNH (22).xlsx")
    rawData = rawData[feild]
    
    output = []
    column = [i for i in rawData]
    print(column)
    for index, row in rawData.iterrows():
        pickData = {'type': outputName}

        idName = "Fish_{}".format(str(row['Internal ID']).zfill(5))
        # diveFishName[idName]['zh-tw']

        pickData['id'] = int(row['#'])
        pickData['name_c'] = nameMap[idName]['zh-tw']
        pickData['name_j'] = nameMap[idName]['ja-jp']
        pickData['name_e'] = nameMap[idName]['en-us']

        pickData['Sell'] = int(row['Sell'])
        pickData['Where/How'] = where[row['Where/How']]
        pickData['Shadow'] = shadow[row['Shadow']]
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