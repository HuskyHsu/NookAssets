import math

import parse

if __name__ == '__main__':

    outputName = 'tools'

    toolName_TWzh = parse.getLanguageMap('String_TWzh/Item/STR_ItemName_20_Tool', True)
    toolName_JPja = parse.getLanguageMap('String_JPja/Item/STR_ItemName_20_Tool', True)
    etcName_TWzh = parse.getLanguageMap('String_TWzh/Item/STR_ItemName_80_Etc', True)
    etcName_JPja = parse.getLanguageMap('String_JPja/Item/STR_ItemName_80_Etc', True)
    

    nameMapCustom = parse.getCustomLanguageMap()    

    def getName(idName):
        if idName in toolName_TWzh:
            return {
                'zh-tw': toolName_TWzh[idName],
                'ja-jp': toolName_JPja[idName]
            }
        if idName in etcName_TWzh:
            return {
                'zh-tw': etcName_TWzh[idName],
                'ja-jp': etcName_JPja[idName]
            }
        else:
            print(idName)

    rawData = parse.getRawData()

    BodyParts = parse.getLanguageMap('String_TWzh/Remake/STR_Remake_BodyParts', True)
    BodyColor = parse.getLanguageMap('String_TWzh/Remake/STR_Remake_BodyColor', True)
    # translations = parse.readExcel('./rawData/Translations - 1.4.0.xlsx')
    # materialName = parse.getLanguage(translations['Craft'], 'English')
    # materialName_2 = parse.getLanguage(translations['Plants'], 'English')
    # NPCsName = parse.getLanguage(translations['Special NPCs'], 'English')

    output = {}
    for index, row in rawData['Tools'].iterrows():
        idName = str(row['Internal ID']).zfill(5)

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
            pickData['type'] = 'tools'
            pickData['name_c'] = name['zh-tw']
            pickData['name_j'] = name['ja-jp']
            pickData['name_e'] = row['Name']
            
        #     pickData['buy'] = None if type(row['Buy']) == str else row['Buy']
        #     pickData['sell'] = row['Sell']
        #     pickData['category'] = categoryName[1]
        #     pickData['tag'] = nameMapCustom[row['Tag']]['zh-tw']

        #     pickData['themes'] = []
        #     if row['HHA Concept 1'] != 'None':
        #         pickData['themes'].append(nameMapCustom[row['HHA Concept 1']]['zh-tw'])
        #     if row['HHA Concept 2'] != 'None':
        #         pickData['themes'].append(nameMapCustom[row['HHA Concept 2']]['zh-tw'])

        #     pickData['interact'] = True if row['Interact'] == 'Yes' else False
        #     pickData['size'] = row['Size']
        #     pickData['obtainedFrom'] = nameMapCustom[row['Source']]['zh-tw']

        #     pickData['DIY'] = True if row['DIY'] == 'Yes' else False
        #     if row['DIY'] == 'Yes': 
        #         pickData['diyInfoMaterials'] = recipeMap[row['Internal ID']]['diyInfoMaterials']
        #         pickData['diyInfoObtainedFrom'] = recipeMap[row['Internal ID']]['diyInfoObtainedFrom']
        #         pickData['diyInfoSourceNotes'] = recipeMap[row['Internal ID']]['diyInfoSourceNotes']
        #     else:
        #         pickData['diyInfoMaterials'] = None
        #         pickData['diyInfoObtainedFrom'] = None
        #         pickData['diyInfoSourceNotes'] = None

        #     pickData['bodyTitle'] = BodyParts[idName] if str(row['Body Title']) != 'nan' else '無'
        #     pickData['patternTitle'] = FabricParts[idName] if str(row['Pattern Title']) != 'nan' else '無'
        #     pickData['bodyCustomize'] = True if row['Body Customize'] == 'Yes' else False
        #     pickData['patternCustomize'] = True if row['Pattern Customize'] == 'Yes' else False

        #     pickData['filename'] = row['Filename']
        #     pickData['version'] = row['Version Added']

            pickData['variations'] = {'bodys': {}, 'pattrens': {}}

        if variantId is not None and str(row['Variation']) != 'nan':
            bodyKey = '{}_{}'.format(idName, variantId[0])
            pickData['variations']['bodys'][BodyColor[bodyKey]] = variantId[0]

        output[pickData['id']] = pickData

    #     pickData['filename'] = row['Icon Filename']
    output = list(output.values())
    output = sorted(output, key=lambda k: k['id'])

    parse.saveFile(outputName, output)