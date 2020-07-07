import math

import parse

if __name__ == '__main__':

    feild = 'Sea Creatures'
    outputName = 'seaCreatures'

    shadow = {
        'Large': '大',
        'Small': '小',
        'Medium': '中',
        'X-Small': '極小',
        'X-Large': '特大'
    }

    speed = {
        'Stationary': '固定',
        'Very slow': '非常慢',
        'Slow': '慢',
        'Medium': '中',
        'Fast': '快',
        'Very fast': '非常快'
    }

    translations = parse.readExcel('./rawData/Translations - 1.3.0.xlsx')
    diveFishName = parse.getLanguage(translations[feild])
    # print(diveFishName)

    rawData = parse.readExcel("./rawData/Editors' Copy - Data Spreadsheet for ACNH (22).xlsx")
    rawData = rawData[feild]
    
    output = []
    column = [i for i in rawData]
    print(column)
    for index, row in rawData.iterrows():
        pickData = {'type': outputName}

        idName = "DiveFish_{}".format(str(row['Internal ID']).zfill(5))
        # diveFishName[idName]['zh-tw']

        pickData['id'] = int(row['#'])
        pickData['name_c'] = diveFishName[idName]['zh-tw']
        pickData['name_j'] = diveFishName[idName]['ja-jp']
        pickData['name_e'] = diveFishName[idName]['en-us']

        pickData['Sell'] = int(row['Sell'])
        pickData['Shadow'] = shadow[row['Shadow']]
        pickData['Movement Speed'] = speed[row['Movement Speed']]
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