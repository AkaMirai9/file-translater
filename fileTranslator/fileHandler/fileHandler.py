from io import TextIOWrapper
import os
import json
import threading
import re

from translation.translation import *
from googletrans import Translator


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
    keys = []
    lines = []
    while line != '':
        line = myJSONFile.readline()
        print('line:' + line)
        matches = re.search(
            r"\"(?P<key>[a-zA-Z0-9._-]+)\": ?\"(?P<value>.*)\"(,$|$)", line)
        if matches != None:
            newDict[matches['key']] = matches['value']
            keys.append(matches['key'])
            lines.append(matches['value'])
    # return (keys, lines)
    return newDict


def createAllFiles(toTranslate: str):
    languages = getLanguages()
    srcFile = open(toTranslate, 'r', encoding="utf-8")
    srcJSON = JSONToDict(srcFile)
    print(srcJSON)
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
        thread = threading.Thread(
            target=translateLanguage, args=(srcJSON, src, folder, file))
        treadList.append(thread)
        # translateLanguage(srcJSON, src, folder, file)
        os.chdir('..')

    for i in range(0, len(treadList) - 1, 2):
        currentThreadList = [treadList[i]]
        if i + 1 < len(treadList):
            currentThreadList.append(treadList[i + 1])
        if i + 2 < len(treadList):
            currentThreadList.append(treadList[i + 2])

        for thread in currentThreadList:
            thread.start()

        for thread in currentThreadList:
            thread.join()
