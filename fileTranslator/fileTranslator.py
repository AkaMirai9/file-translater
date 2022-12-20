import sys

from errorHandler.isEntryValid import isEntryValid
from fileHandler.fileHandler import *


def main():
    isEntryValid(sys.argv)
    createAllFiles(sys.argv[1])


if __name__ == "__main__":
    main()
