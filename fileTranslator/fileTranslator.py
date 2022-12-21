import sys

from errorHandler.isEntryValid import isEntryValid
from fileHandler.fileHandler import *


def main():
    isEntryValid(sys.argv)
    createAllFiles(sys.argv[1])
    print("L'ensemble de vos traductions se trouvent dans le fichier result")


if __name__ == "__main__":
    main()
