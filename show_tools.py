import tkinter as tk

class ShowTools(tk.LabelFrame):
    """
    Allows to diplay other panels
    """

    def __init__(self, master, main_application):
        super().__init__(master, text="Show tools")
        self.master = master
        self.main_application = main_application

        self.button_timeline = tk.Button(self, text="Show timeline", command=self.show_timeline)
        self.button_taskmanager = tk.Button(self, text="Show tasks manager", command=self.show_taskmanager)
        self.button_graph = tk.Button(self, text="Create new graph window", command=self.show_graph)

        self.button_timeline.grid(row=1)
        self.button_taskmanager.grid(row=2)        
        self.button_graph.grid(row=3)

        self.master.protocol("WM_DELETE_WINDOW", lambda:None)

    def has_toplevel(self, widget):
        return tk.Toplevel.winfo_exists(widget.master)

    def show_timeline(self):
        if self.has_toplevel(self.main_application.timeline):
            self.main_application.timeline.focus_set()
        else:
            self.main_application.make_timeline()
    
    def show_taskmanager(self):
        if self.has_toplevel(self.main_application.task_manager):
            self.main_application.task_manager.focus_set()
        else:
            self.main_application.make_taskmanager()
    
    def show_graph(self):
        self.main_application.make_graph()