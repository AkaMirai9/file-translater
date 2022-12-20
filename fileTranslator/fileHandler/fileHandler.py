import os
import json

from translation.translation import translateLanguage


def removeBreakLine(string: str):
    language = string[0: -1]
    if language.__len__() != 2:
        exit('Le Fichier languages.txt est mal formaté')
    return language


def getLanguages():
    languagesFile = open('languages.txt', 'r')
    languages = [removeBreakLine(x) for x in languagesFile.readlines()]
    languagesFile.close()
    return languages


def createAllFiles(toTranslate: str):
    languages = getLanguages()
    srcFile = open(toTranslate, 'r')
    srcJSON = json.load(srcFile)
    try:
        os.mkdir('result')
    except FileExistsError:
        pass
    os.chdir('result')
    src = toTranslate[-7: -5]
    print(src)
    for folder in languages:
        try:
            os.mkdir(folder)
        except FileExistsError:
            pass
        os.chdir(folder)
        file = open(folder + '.json', 'w', encoding='utf-8')
        translateLanguage(srcJSON, src, folder, file)
        file.close()
        os.chdir('..')
