import os

def clearScreen():
    if os.name == "posix":
        return os.system('clear')
    return os.system('cls')

def clearPrint(obj):
    clearScreen()
    print(obj)
    input()