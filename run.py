import sys
from main import *


if __name__ == "__main__":
    try:
        if sys.argv[1] == "manual":
            default = False
            main(default)
        elif sys.argv[1] == "help":
            showHelp()
    except IndexError:
        default = True
        main(default)
