import math

import parse

if __name__ == '__main__':

    feild = 'Furniture'
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

    rawData = parse.readExcel("./rawData/Data Spreadsheet for Animal Crossing New Horizons.xlsx")

    translations = parse.readExcel('./rawData/Translations - 1.4.0.xlsx')
    materialName = parse.getLanguage(translations['Craft'], 'English')
    materialName_2 = parse.getLanguage(translations['Plants'], 'English')
    NPCsName = parse.getLanguage(translations['Special NPCs'], 'English')
    
    recipeMap = {}
    for  index, recipe  in rawData['Recipes'].iterrows():
        pickData = {}
        pickData['diyInfoMaterials'] = []

        for i in range(1, 6):
            if str(recipe['Material {}'.format(i)]) != 'nan':

                if recipe['Material {}'.format(i)] in materialName:
                    name = materialName[recipe['Material {}'.format(i)]]
                elif recipe['Material {}'.format(i)] in materialName_2:
                    name = materialName_2[recipe['Material {}'.format(i)]]

                pickData['diyInfoMaterials'].append(
                    {
                        'count': recipe['#{}'.format(i)], 
                        'itemName': name['zh-tw']
                    }
                )

        # print(recipe['Source Notes'])
        pickData['diyInfoObtainedFrom'] = '; '.join([nameMapCustom[s]['zh-tw'] for s in recipe['Source'].split('; ')])
        try:
            pickData['diyInfoSourceNotes'] = nameMapCustom[recipe['Source Notes']]['zh-tw'] if str(recipe['Source Notes']) != 'nan' else None
        except:
            print(recipe['Source Notes'])
            pickData['diyInfoSourceNotes'] = recipe['Source Notes']
        

        recipeMap[recipe['Crafted Item Internal ID']] = pickData


    # "Image", "Variation", "Body Title", "Pattern", "Pattern Title", "DIY", "Body Customize", "Pattern Customize", "Kit Cost", "Buy", "Sell", "Color 1", "Color 2", "Size", "Surface", "Miles Price", "Source", "Source Notes", "HHA Base Points", "HHA Concept 1", "HHA Concept 2", "HHA Series", "HHA Set", "HHA Category", "Interact", "Tag", "Outdoor", "Speaker Type", "Lighting Type", "Catalog", "Version Added", "Version Unlocked", "Filename", "Variant ID", "Internal ID"

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
                if row['HHA Concept 1'] != 'None':
                    pickData['themes'].append(nameMapCustom[row['HHA Concept 1']]['zh-tw'])
                if row['HHA Concept 2'] != 'None':
                    pickData['themes'].append(nameMapCustom[row['HHA Concept 2']]['zh-tw'])

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