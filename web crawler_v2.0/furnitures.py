import math

import parse

if __name__ == '__main__':

    outputName = 'furnitures'

    furnitureName_TWzh = parse.getLanguageMap('String_TWzh/Item/STR_ItemName_00_Ftr')
    furnitureName_JPja = parse.getLanguageMap('String_JPja/Item/STR_ItemName_00_Ftr')

    insectToyName_TWzh = parse.getLanguageMap('String_TWzh/Item/STR_ItemName_36_InsectToy')
    insectToyName_JPja = parse.getLanguageMap('String_JPja/Item/STR_ItemName_36_InsectToy')

    fishToyName_TWzh = parse.getLanguageMap('String_TWzh/Item/STR_ItemName_37_FishToy')
    fishToyName_JPja = parse.getLanguageMap('String_JPja/Item/STR_ItemName_37_FishToy')

    houseDoorDecoName_TWzh = parse.getLanguageMap('String_TWzh/Item/STR_ItemName_61_HouseDoorDeco')
    houseDoorDecoName_JPja = parse.getLanguageMap('String_JPja/Item/STR_ItemName_61_HouseDoorDeco')

    nameMapCustom = parse.getCustomLanguageMap()    

    def getName(idName):
        if idName in furnitureName_TWzh:
            return {
                'zh-tw': furnitureName_TWzh[idName],
                'ja-jp': furnitureName_JPja[idName]
            }
        elif idName in insectToyName_TWzh:
            return {
                'zh-tw': insectToyName_TWzh[idName],
                'ja-jp': insectToyName_JPja[idName]
            }
        elif idName in fishToyName_TWzh:
            return {
                'zh-tw': fishToyName_TWzh[idName],
                'ja-jp': fishToyName_JPja[idName]
            }
        elif idName in houseDoorDecoName_TWzh:
            return {
                'zh-tw': houseDoorDecoName_TWzh[idName],
                'ja-jp': houseDoorDecoName_JPja[idName]
            }
        else:
            print(idName)

    BodyParts = parse.getLanguageMap('String_TWzh/Remake/STR_Remake_BodyParts')
    BodyColor = parse.getLanguageMap('String_TWzh/Remake/STR_Remake_BodyColor')
    FabricParts = parse.getLanguageMap('String_TWzh/Remake/STR_Remake_FabricParts')
    FabricColor = parse.getLanguageMap('String_TWzh/Remake/STR_Remake_FabricColor')
    FabricColorCommon = parse.getLanguageMap('String_TWzh/Remake/STR_Remake_FabricColorCommon')

    rawData = parse.getRawData()
    recipeMap = parse.getRecipe()
    series = parse.getSeries()

    categoryNames = [
        ['Housewares', '家具'],
        ['Miscellaneous', '小物件'],
        ['Wall-mounted', '壁掛物']
    ]

    output = {}
    for categoryName in categoryNames:
        category = rawData[categoryName[0]]
    
        # column = [i for i in category]
        # print(column)
        for index, row in category.iterrows():
            idName = "Ftr_{}".format(str(row['Internal ID']).zfill(5))

            if row['Tag'] == 'Insect':
                idName = idName.replace('Ftr', 'InsectToy')
            elif row['Tag'] == 'Fish':
                idName = idName.replace('Ftr', 'FishToy')
            elif row['Tag'] == 'House Door Decor':
                idName = idName.replace('Ftr', 'DoorDeco')

            name = getName(idName)
            if name is None:
                idName = idName.replace('FishToy', 'Ftr').replace('InsectToy', 'Ftr')
                name = getName(idName)

            if '_' in str(row['Variant ID']):
                variantId = row['Variant ID'].split('_')
            else:
                variantId = None

            if row['Internal ID'] in output:
                pickData = output[row['Internal ID']]
            else:
                pickData = {}
            
                pickData['id'] = row['Internal ID']
                pickData['type'] = 'furnitures'
                pickData['name_c'] = name['zh-tw']
                pickData['name_j'] = name['ja-jp']
                pickData['name_e'] = row['Name']
                
                pickData['buy'] = None if type(row['Buy']) == str else row['Buy']
                pickData['sell'] = row['Sell']
                pickData['category'] = categoryName[1]
                pickData['tag'] = nameMapCustom[row['Tag']]['zh-tw']
                
                pickData['themes'] = []
                if row['HHA Concept 1'] != 'None' and row['HHA Concept 1'] != 'none':
                    pickData['themes'].append(nameMapCustom[row['HHA Concept 1']]['zh-tw'])
                if row['HHA Concept 2'] != 'None' and row['HHA Concept 2'] != 'none':
                    pickData['themes'].append(nameMapCustom[row['HHA Concept 2']]['zh-tw'])
            
                pickData['series'] = series[row['HHA Series'].strip(' ')]

                pickData['interact'] = True if row['Interact'] == 'Yes' else False
                pickData['size'] = row['Size']
                pickData['obtainedFrom'] = nameMapCustom[row['Source']]['zh-tw']

                pickData['DIY'] = True if row['DIY'] == 'Yes' else False
                if row['DIY'] == 'Yes':
                    pickData['diyInfoMaterials'] = recipeMap[row['Internal ID']]['diyInfoMaterials']
                    pickData['diyInfoObtainedFrom'] = recipeMap[row['Internal ID']]['diyInfoObtainedFrom']
                    pickData['diyInfoSourceNotes'] = recipeMap[row['Internal ID']]['diyInfoSourceNotes']
                else:
                    pickData['diyInfoMaterials'] = None
                    pickData['diyInfoObtainedFrom'] = None
                    pickData['diyInfoSourceNotes'] = None

                pickData['bodyTitle'] = BodyParts[idName] if str(row['Body Title']) != 'nan' else '無'
                pickData['patternTitle'] = FabricParts[idName] if str(row['Pattern Title']) != 'nan' else '無'
                pickData['bodyCustomize'] = True if row['Body Customize'] == 'Yes' else False
                pickData['patternCustomize'] = True if row['Pattern Customize'] == 'Yes' else False

                pickData['filename'] = row['Filename']
                pickData['version'] = row['Version Added']

                pickData['variations'] = {'bodys': {}, 'pattrens': {}}

            if variantId is not None and str(row['Variation']) != 'nan':
                bodyKey = '{}_{}'.format(idName, variantId[0])
                pickData['variations']['bodys'][BodyColor[bodyKey]] = variantId[0]

            if variantId is not None and str(row['Pattern']) != 'nan':
                bodyKey = '{}_{}'.format(idName, variantId[1])
                pickData['variations']['pattrens'][FabricColor[bodyKey]] = variantId[1]

            output[pickData['id']] = pickData

    #     pickData['filename'] = row['Icon Filename']
    output = list(output.values())
    output = sorted(output, key=lambda k: k['id'])

    parse.saveFile(outputName, output)