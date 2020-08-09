import math

import parse

if __name__ == '__main__':

    outputName = 'tools'

    typeSource = ['STR_ItemName_20_Tool', 'STR_ItemName_80_Etc', 'STR_ItemName_19_Umbrella']

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

    nameMapCustom = parse.getCustomLanguageMap()    
    rawData = parse.getRawData()
    recipeMap = parse.getRecipe()

    BodyParts = parse.getLanguageMap('String_TWzh/Remake/STR_Remake_BodyParts', True)
    BodyColor = parse.getLanguageMap('String_TWzh/Remake/STR_Remake_BodyColor', True)

    categoryNames = [
        ['Tools', '工具'],
        ['Umbrellas', '雨傘']
    ]

    output = {}
    for categoryName in categoryNames:
        category = rawData[categoryName[0]]

        for index, row in category.iterrows():
            idName = str(row['Internal ID']).zfill(5)

            name = getName(idName)

            if 'Variant ID' in row and '_' in str(row['Variant ID']):
                variantId = row['Variant ID'].split('_')
            else:
                variantId = None

            if row['Internal ID'] in output:
                pickData = output[row['Internal ID']]
            else:
                pickData = {}
            
                pickData['id'] = row['Internal ID']
                pickData['type'] = 'tools'
                pickData['category'] = categoryName[1]
                pickData['name_c'] = name['zh-tw']
                pickData['name_j'] = name['ja-jp']
                pickData['name_e'] = row['Name']

                if 'Uses' in row:
                    pickData['uses'] = None if str(row['Uses']) == 'Unlimited' else row['Uses']
                else:
                    pickData['uses'] = None
                
                pickData['buy'] = None if type(row['Buy']) == str else row['Buy']
                pickData['sell'] = row['Sell']
                pickData['obtainedFrom'] = [nameMapCustom[s]['zh-tw'] for s in row['Source'].split('; ')]
                pickData['sourceNotes'] = nameMapCustom[row['Source Notes']]['zh-tw'] if str(row['Source Notes']) != 'nan' else None

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

                pickData['variations'] = {'bodys': {}, 'pattrens': {}}

            if variantId is not None and str(row['Variation']) != 'nan':
                bodyKey = '{}_{}'.format(idName, variantId[0])
                pickData['variations']['bodys'][BodyColor[bodyKey]] = variantId[0]

            output[pickData['id']] = pickData

    #     pickData['filename'] = row['Icon Filename']
    output = list(output.values())
    output = sorted(output, key=lambda k: k['id'])

    parse.saveFile(outputName, output)