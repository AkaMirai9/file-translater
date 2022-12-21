from io import TextIOWrapper
import os
import json
import threading
import re

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

def JSONToDict(myJSONFile: TextIOWrapper):
    newDict = dict()
    line = myJSONFile.readline()
    while line != '':
        line = myJSONFile.readline()
        print('line:' + line )
        if str(type(re.search(r"{\n|}\n|}|^$", line))) != "<class 'NoneType'>":
            continue
        matches = re.search(r"^  \"(?P<key>[a-zA-Z0-9._-]+)\": ?\"(?P<value>.*)\"(,$|$)", line)
        print('matches:')
        print(matches)
        newDict[matches['key']] = matches['value']
    return newDict


def createAllFiles(toTranslate: str):
    languages = getLanguages()
    srcFile = open(toTranslate, 'r')
    srcJSON = JSONToDict(srcFile)
    try:
        os.mkdir('result')
    except FileExistsError:
        pass
    os.chdir('result')
    src = toTranslate[-7: -5]
    print('Langue source: ' + src +
          '\nListe des langues dans lesquelles le fichier va être traduit:\n')
    treadList = []
    fileList = []
    for folder in languages:
        try:
            os.mkdir(folder)
        except FileExistsError:
            pass
        os.chdir(folder)
        file = open('translation.json', 'w', encoding='utf-8')
        fileList.append(file)
        treadList.append(threading.Thread(
            target=translateLanguage, args=(srcJSON, src, folder, file)))
        os.chdir('..')

    for thread in treadList:
        thread.start()
