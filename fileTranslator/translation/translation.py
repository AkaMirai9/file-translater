from io import TextIOWrapper
import json
import os

import translators as ts
import translators.server as tss


def translateLanguage(srcJSON: dict, src: str, dest: str, fileDest: TextIOWrapper):
    if src != dest:
        print(dest)
        newDico = dict()
        for item in srcJSON.keys():
            newDico[item] = tss.google(
                srcJSON[item], src, dest)
        print(newDico)
        json.dump(newDico, fileDest, ensure_ascii=False)
    else:
        json.dump(srcJSON, fileDest, ensure_ascii=False)
