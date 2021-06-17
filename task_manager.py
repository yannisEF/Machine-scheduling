import tkinter as tk

class TaskManager(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        # Right : tasks parameters (distributions)
        # Left: machine selector -> machine1, machine2, ... allMachines