import tkinter as tk

class Canvas(tk.Canvas):
    """
    Main display of application, shows machines executing tasks
    """

    parameters = {"width": 800,
                  "height": 600,
                  "bg": "black", }

    machine_size = 50
    machine_margin = (75, 50, 50) # margin with borders, x, y, and next machine
    machine_color = "lightblue"

    task_size = 25
    task_margin = (50, 25)  # margin with machine, with next task
    task_colors = {"working": "yellow",
                   "paused": "red",
                   "finished": "green", }
    
    text_size = 8
    text_margin = 13
    text_color = "white"    
    text_font = "Trebuchet MS"

    scroll_sensitivity = (10, 25)
    view_margin = (25, 25)

    def __init__(self, master, main_application, machines=[]):
        super().__init__(master, **Canvas.parameters)
        self.master = master
        self.main_application = main_application

        self.object_to_id = {}
        self.id_to_object = {}

        self.task_to_text_length = {}

        self.machines = []
        self.machine_to_display = {}        
        self.tasks = []  
      
        for m in machines:
            self.add_machine(m)
            self.tasks += list(m.allTasks.values())

        self.view_offset_x, self.view_offset_y = 0, 0

        self.draw_machines()

        self.bind("<Left>", lambda x: self.scroll_view(x, (1,0)))
        self.bind("<Right>", lambda x: self.scroll_view(x, (-1,0)))
        self.bind("<Up>", lambda x: self.scroll_view(x, (0,1)))
        self.bind("<Button-4>", lambda x: self.scroll_view(x, (0,1)))
        self.bind("<Down>", lambda x: self.scroll_view(x, (0,-1)))
        self.bind("<Button-5>", lambda x: self.scroll_view(x, (0,-1)))

        self.focus_set()

    def add_machine(self, machine):
        self.machines.append(machine)
        self.machine_to_display[machine] = []

    def clear_display(self):
        self.delete('all')

    def draw_machines(self):
        """
        Draws all machines
        """
        # TO-DO : Need to discriminate with machine's type for display

        self.clear_display()

        x1, y1, _ = Canvas.machine_margin
        x2, y2 = x1 + Canvas.machine_size, y1 + Canvas.machine_size

        x1 += self.view_offset_x 
        x2 += self.view_offset_x
        y1 += self.view_offset_y
        y2 += self.view_offset_y

        for k in range(len(self.machines)):
            machine_id = self.create_rectangle(x1, y1, x2, y2,
                fill=Canvas.machine_color)
            
            y1 = y2 + Canvas.machine_margin[2]
            y2 = y1 + Canvas.machine_size

            self.object_to_id[self.machines[k]] = machine_id
            self.id_to_object[machine_id] = self.machines[k]

            self.draw_tasks(machine_id)

    def draw_tasks(self, machine_id):
        """
        Draws all tasks of a machine
        """

        x1, y1, x2, y2 = self.coords(machine_id)
        x1 += Canvas.machine_size + Canvas.task_margin[0]
        y1 += round((Canvas.machine_size - Canvas.task_size)/2)
        x2, y2 = x1 + Canvas.task_size, y1 + Canvas.task_size

        machine = self.id_to_object[machine_id]
        for task in machine.allTasks.values():
            if task.status != "unavailable" and task not in self.machine_to_display[machine]:
                self.machine_to_display[machine].append(task)
        for task in machine.finishedTasks.values():
            try:
                self.machine_to_display[machine].remove(task)
            except ValueError:
                pass
            
        for task in self.machine_to_display[machine]:
            task_id = self.create_oval(
                x1, y1, x2, y2, fill=Canvas.task_colors[task.status])
            
            if task.status != "finished" and task.currentStep > 0:
                extent = int(360 * task.currentStep / task.realLength)
                fill = Canvas.task_colors["finished"] if task.status == "working" else Canvas.task_colors["paused"]
                pogress_id = self.create_arc(x1, y1, x2, y2, fill=fill, start=90, extent=extent)
            
            x1 += Canvas.task_size + Canvas.task_margin[1]
            x2 = x1 + Canvas.task_size

            self.object_to_id[task] = task_id
            self.id_to_object[task_id] = task

            self.draw_length(task)

    def draw_length(self, task):
        """
        Draws the lengths of a task, [real, predicted]
        """

        x1, y1, x2, y2 = self.coords(self.object_to_id[task])
        text = "[{}, {}]".format(task.realLength, task.predLength)

        x, y = round((x1 + x2)/2), y2 + Canvas.text_margin
        text_id = self.create_text(x, y, anchor=tk.CENTER, text=text, fill=Canvas.text_color, font=(Canvas.text_font, Canvas.text_size))

        self.task_to_text_length[task] = text_id

    def _make_frame(self):
        self.clear_display()
        self.draw_machines()

    def scroll_view(self, event, direction=(0,0)):
        self.view_offset_x += Canvas.scroll_sensitivity[0] * direction[0]
        self.view_offset_y += Canvas.scroll_sensitivity[1] * direction[1]

        if self.view_offset_x > 0:  self.view_offset_x = 0
        if self.view_offset_y > 0:  self.view_offset_y = 0

        self._make_frame()

    def run(self, event):
        for m in self.machines:
            m.run(1)

        self._make_frame()