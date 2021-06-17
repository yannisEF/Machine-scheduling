import os
import random

from distribution import distrib
from task import Task

def clearScreen():
    if os.name == "posix":
        return os.system('clear')
    return os.system('cls')

def clearPrint(obj):
    clearScreen()
    print(obj)
    input()

def randomTasks(a, b):
    return [Task(distrib) for _ in range(random.randint(a, b))]
