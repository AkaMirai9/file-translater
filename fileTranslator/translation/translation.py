from io import TextIOWrapper
import json
from google_trans_new import google_translator
from googletrans import Translator
import deepl

import re
import time

from proxies.proxies import *


def isVariableInside(line):
    return re.search(r"{{(?P<var>.*)}}", line)


def translateLine(line, src, dest):
    if len(line) == 0:
        return ''
    translator = deepl.Translator(
        "31b38853-e3ed-b2dc-e77b-dd8c62c593a8:fx")
    target_lang = dest
    if dest == 'en':
        target_lang = 'en-br'
    if dest == 'pt':
        target_lang = 'pt-pt'
    test = isVariableInside(line)
    try:
        translation = translator.translate_text(
            text=line, source_lang=src, target_lang=target_lang)
        if (test != None):
            str(translation).replace(
                re.search(r"{{(?P<var>.*)}}", str(translation))['var'], test['var'])
        return str(translation)
    except:
        translator = Translator(proxies=getProxies())
        if target_lang == 'en-br':
            target_lang = 'en'
        if target_lang == 'pt-pt':
            target_lang = 'pt'
        try:
            translation = translator.translate(line, src=src, dest=target_lang)
            if (test != None):
                str(translation).replace(
                    re.search(r"{{(?P<var>.*)}}", str(translation))['var'], test['var'])
            return str(translation)
        except:
            translator = Translator()
            translation = translator.translate(line, src=src, dest=target_lang)
            if (test != None):
                str(translation).replace(
                    re.search(r"{{(?P<var>.*)}}", str(translation))['var'], test['var'])
            return str(translation)


def tupleToDict(dico, tuples):
    print('len(tuples[0]): ', len(tuples[0]))
    print('len(tuples[1]): ', len(tuples[1]))
    for i in range(len(tuples[0]) - 1):
        dico[tuples[0][i]] = tuples[1][i]
    return dico


def googleTranslation(tuples: tuple, src: str, dest: str, fileDest: TextIOWrapper):
    keys = tuples[0]
    lines = tuples[1]
    dico = dict()
    translator = google_translator()
    total = 0
    for i in range(len(lines)):
        print(lines[i])
        total += len(lines[i])
        translation = translator.translate(
            lines[i], src=src, dest=dest)
        dico[keys[i]] = translation
        print(dest + ':' + str(i) + '/' + str(len(lines)))
        if i % 25 == 0:
            time.sleep(5)
        if total > 4900:
            time.sleep(25)
            total = 0

    json.dump(dico, fileDest, ensure_ascii=False)
    fileDest.close()


def translateLanguage(srcJSON: dict, src: str, dest: str, fileDest: TextIOWrapper):
    # threading.currentThread().setName(dest)
    if src != dest:
        srcLen = srcJSON.keys().__len__()
        index = 0
        print(dest)
        newDico = dict()
        for item in srcJSON.keys():
            newDico[item] = translateLine(
                srcJSON[item], src, dest)
            index += 1
            # if threading.currentThread().getName() == 'en':
            #     if index == 1:
            #         print('\n')
            #     print('Avancement: ' + str(index) + '/' +
            #           str(srcLen) + ' champs traduits')
            #     if index == srcLen:
            #         print('\nCréation des Fichiers en cours')
            if index % 75 == 0:
                time.sleep(65)
            print(dest + ':' + str(index) + '/' + str(srcLen))
        json.dump(newDico, fileDest, ensure_ascii=False)
    else:
        json.dump(srcJSON, fileDest, ensure_ascii=False)

    fileDest.close()
