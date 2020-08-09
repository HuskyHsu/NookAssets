import math

import parse

if __name__ == '__main__':

    outputName = 'homeStyle'

    series = parse.getSeries()

    typeSource = ['STR_ItemName_50_RoomWall', 'STR_ItemName_51_RoomFloor', 'STR_ItemName_52_RoomRug']

    nameMaps = []
    for t in typeSource:
        TWzhFile = f'String_TWzh/Item/{t}'
        JPjaFile = f'String_JPja/Item/{t}'

        name_TWzh = parse.getLanguageMap(TWzhFile, True)
        name_JPja = parse.getLanguageMap(JPjaFile, True)

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
        ['Wallpaper', '壁紙'],
        ['Floors', '地板'],
        ['Rugs', '地毯']
    ]

    output = {}
    for categoryName in categoryNames:
        category = rawData[categoryName[0]]
    
        # column = [i for i in category]
        # print(column)
        for index, row in category.iterrows():
            idName = str(row['Internal ID']).zfill(5)

            name = getName(idName)

            pickData = {}
        
            pickData['id'] = row['Internal ID']
            pickData['type'] = outputName
            pickData['category'] = categoryName[1]
            pickData['name_c'] = name['zh-tw']
            pickData['name_j'] = name['ja-jp']
            pickData['name_e'] = row['Name']
            
            pickData['obtainedFrom'] = '; '.join([nameMapCustom[s]['zh-tw'] for s in row['Source'].replace('\n', '').split('; ')])
            pickData['buy'] = None if type(row['Buy']) == str else row['Buy']
            pickData['sell'] = row['Sell']

            pickData['themes'] = []
            if row['HHA Concept 1'] != 'None' and row['HHA Concept 1'] != 'none':
                pickData['themes'].append(nameMapCustom[row['HHA Concept 1']]['zh-tw'])
            if row['HHA Concept 2'] != 'None' and row['HHA Concept 2'] != 'none':
                pickData['themes'].append(nameMapCustom[row['HHA Concept 2']]['zh-tw'])

            pickData['series'] = series[row['HHA Series'].strip(' ')]

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

            output[pickData['id']] = pickData

    #     pickData['filename'] = row['Icon Filename']
    output = list(output.values())
    output = sorted(output, key=lambda k: k['id'])

    parse.saveFile(outputName, output)