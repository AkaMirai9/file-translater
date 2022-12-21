from io import TextIOWrapper
import json
import threading

import translators as ts
import translators.server as tss


def translateLanguage(srcJSON: dict, src: str, dest: str, fileDest: TextIOWrapper):
    threading.currentThread().setName(dest)
    if src != dest:
        srcLen = srcJSON.keys().__len__()
        index = 0
        print(dest)
        newDico = dict()
        for item in srcJSON.keys():
            newDico[item] = tss.google(
                srcJSON[item], src, dest)
            index += 1
            if threading.currentThread().getName() == 'en':
                if index == 1:
                    print('\n')
                print('Avancement: ' + str(index) + '/' +
                      str(srcLen) + ' champs traduits')
                if index == srcLen:
                    print('\nCréation des Fichiers en cours')
        json.dump(newDico, fileDest, ensure_ascii=False)
    else:
        json.dump(srcJSON, fileDest, ensure_ascii=False)

    fileDest.close()
