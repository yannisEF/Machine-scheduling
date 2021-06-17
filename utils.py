import os
import random
import tkinter as tk

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

def reset_entry(entry, default_value = None):
    entry.delete(0, len(entry.get()))

    if default_value is not None:
        entry.insert(tk.END, default_value)