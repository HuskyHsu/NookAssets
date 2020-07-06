import pandas as pd

def readExcel(filePath):
    try:
        df = pd.read_excel(filePath, sheetname=None)
    except:
        df = pd.read_excel(filePath, sheet_name=None)
    return df

def getLanguage(df, sheetName):
    language = ['id', 'Chinese (Traditional)', 'English', 'Japanese']

    data = list(map(lambda field: df[sheetName][field].tolist(), language))
    idMap = {}
    for index, id in enumerate(data[0]):
        idMap[id] = {'name_c': data[1][index], 'name_e': data[2][index], 'name_j': data[3][index]}
    
    return idMap

if __name__ == '__main__':

    feild = 'Sea Creatures'
    translations = readExcel('./rawData/Translations - 1.3.0.xlsx')
    diveFish = getLanguage(translations, feild)

    rawData = readExcel("./rawData/Editors' Copy - Data Spreadsheet for ACNH (22).xlsx")
    
    for index, row in rawData[feild].iterrows():
        idName = "DiveFish_{}".format(str(row['Internal ID']).zfill(5))
        print(diveFish[idName]['name_c'])
