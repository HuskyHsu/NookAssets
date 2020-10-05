import math

import parse

if __name__ == '__main__':

    outputName = 'clothes'
    seasonal = {
        "All Year": "全年",
        "Winter": "冬季",
        "Summer": "夏季",
        "Spring": "春季",
        "Fall": "秋季"
    }

    styles = {
        "Simple": "簡單",
        "Cool": "酷感",
        "Cute": "可愛",
        "Active": "活潑",
        "Elegant": "優雅",
        "Gorgeous": "華麗"
    }

    themes = {
        "everyday": "日常生活",
        "fairy tale": "童話世界",
        "formal": "正式",
        "goth": "恐怖",
        "outdoorsy": "戶外活動",
        "party": "派對",
        "comfy": "悠閒",
        "sporty": "運動",
        "theatrical": "舞台",
        "vacation": "度假",
        "work": "工作"
    }


    typeSource = ['Tops', 'Socks', 'Shoes', 'OnePiece', 'MarineSuit', 'Helmet', 'Cap', 'Bottoms', 'Bag', 'Accessory']

    nameMaps = []
    for t in typeSource:
        TWzhFile = f'String_TWzh/Outfit/GroupName/STR_OutfitGroupName_{t}'
        JPjaFile = f'String_JPja/Outfit/GroupName/STR_OutfitGroupName_{t}'

        name_TWzh = parse.getLanguageMap(TWzhFile)
        name_JPja = parse.getLanguageMap(JPjaFile)

        nameMaps.append({
            'TWzh': name_TWzh,
            'JPja': name_JPja
        })

    nameMapCustom = parse.getCustomLanguageMap()

    def getName(idName):
        name = None
        for nameMap in nameMaps:
            if idName in nameMap['TWzh'] and name is None:
                name = {
                    'zh-tw': nameMap['TWzh'][idName],
                    'ja-jp': nameMap['JPja'][idName]
                }
                return name

        print(idName)
        return name

    rawData = parse.getRawData()
    recipeMap = parse.getRecipe()

    categoryNames = [
        ['Tops', '上身'],
        ['Bottoms', '下身'],
        ['Dress-Up', '套裝'],
        ['Headwear', '頭戴物'],
        ['Accessories', '飾品'],
        ['Socks', '襪子'],
        ['Shoes', '鞋子'],
        ['Bags', '包包'],
        ['Clothing Other', '其他服飾']
    ]
    #         ['Umbrellas', '雨傘'],

    output = {}
    for categoryName in categoryNames:
        category = rawData[categoryName[0]]

        # column = [i for i in category]
        # print(column)
        for index, row in category.iterrows():
            idName = str(row['ClothGroup ID']).zfill(3)

            name = getName(idName)

            if row['ClothGroup ID'] in output:
                pickData = output[row['ClothGroup ID']]
                pickData['variations'] += 1
            else:
                pickData = {}

                pickData['id'] = row['ClothGroup ID']
                pickData['type'] = outputName
                pickData['category'] = categoryName[1]
                pickData['name_c'] = name['zh-tw']
                pickData['name_j'] = name['ja-jp']
                pickData['name_e'] = row['Name']

                pickData['obtainedFrom'] = '; '.join([nameMapCustom[s]['zh-tw'] for s in row['Source'].replace('\n', '').split('; ')])
                pickData['buy'] = None if type(row['Buy']) == str else row['Buy']
                pickData['sell'] = row['Sell']

                pickData['seasonalAvailability'] = seasonal[row['Seasonal Availability']]
                pickData['villagerEquippable'] = row['Villager Equippable'] == 'Yes'

                pickData['styles'] = styles[row['Style 1']]
                pickData['themes'] = [themes[t] for t in row['Label Themes'].replace('\n', '').split('; ')]

                pickData['DIY'] = True if row['DIY'] == 'Yes' else False
                if row['DIY'] == 'Yes':
                    pickData['diyInfoMaterials'] = recipeMap[row['Internal ID']]['diyInfoMaterials']
                    pickData['diyInfoObtainedFrom'] = recipeMap[row['Internal ID']]['diyInfoObtainedFrom']
                    pickData['diyInfoSourceNotes'] = recipeMap[row['Internal ID']]['diyInfoSourceNotes']
                else:
                    pickData['diyInfoMaterials'] = None
                    pickData['diyInfoObtainedFrom'] = None
                    pickData['diyInfoSourceNotes'] = None


                pickData['filename'] = row['Filename']
                pickData['version'] = row['Version Added']

                pickData['variations'] = 1

            output[pickData['id']] = pickData

    #     pickData['filename'] = row['Icon Filename']
    output = list(output.values())
    output = sorted(output, key=lambda k: k['id'])

    parse.saveFile(outputName, output)