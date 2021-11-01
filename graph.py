import tkinter as tk

class Graph(tk.Canvas):
    """
    Displays realtime information about the application
    """

    parameters = {"width":500, 
                "height":375,
                "bg":"white",}
    
    lines_colors = ['blue', 'red', 'green', 'orange',
                    'brown', 'lightblue', 'lightred', 'lightgreen']
    
    lines_margin = (0, 25)

    def __init__(self, master, main_application, recipients, name_x, name_y):
        super().__init__(master, **Graph.parameters)
        self.master = master
        self.main_application = main_application

        self.recipients = recipients
        self.name_x, self.name_y = name_x, name_y

        self.recipient_to_color = {self.recipients[k]:Graph.lines_colors[k%len(Graph.lines_colors)] for k in range(len(self.recipients))}
        self.recipient_to_points = {r:[(0,0)] for r in self.recipients}
        self.recipient_to_draw = {r:[] for r in self.recipients}

        self.max_x, self.max_y = None, None

    def _clear_display(self):
        self.delete('all')
    
    def _draw_borders(self):
        pass
    
    def _retrieve_data(self):
        for r in self.recipients:
            if r == "All machines":
                val = sum([len(k.finishedTaks) for k in self.main_application.machines])
                self.recipient_to_points[r].append(val)
    
    def _add_to_draw(self, recipient):
        try:
            point1, point2 = self.recipient_to_points[recipient][-2:]
            line_id = self.create_line(*point1, *point2, fill=self.recipient_to_color[recipient])
            self.recipient_to_draw[recipient].append(line_id)
        except ValueError:
            pass

    def update_graph(self):
        self._clear_display()
        self._draw_borders()
        self._retrieve_data()

        for r in self.recipients:
            self._add_to_draw(r)


class ShowGraph(tk.Frame):
    """
    Allows to display a graph
    """

    x_options = ["Time elapsed",
                "Real length",
                "Predicted length",
                "Arrival time",]

    y_options = ["Average wait time",
                "Number of tasks"]

    incompatibility = {}

    def __init__(self, master, main_application):
        super().__init__(master)
        self.master = master
        self.main_application = main_application

        self.recipient = tk.StringVar(value="All machines")
        self.x = tk.StringVar(value="X")
        self.y = tk.StringVar(value="Y")

        self.frame_options = tk.LabelFrame(self, text="Options")
        
        # OptionMenu
        self.available_machines = ["All machines"] + ["{} {}".format(m.name, m.id) for m in self.main_application.machines]
        self.menu_choose_machine = tk.OptionMenu(self.frame_options, self.recipient, *self.available_machines)

        # Optionmenu X
        self.available_x = ShowGraph.x_options[:]
        self.menu_choose_x = tk.OptionMenu(self.frame_options, self.x, *self.available_x, command=self.check_x_to_y)

        # Option menu Y
        self.available_y = ShowGraph.y_options[:]
        self.menu_choose_y = tk.OptionMenu(self.frame_options, self.y, *self.available_y, command=self.check_y_to_x)

        # Show graph button
        self.is_shown = False
        self.button_show_graph = tk.Button(self.frame_options, text="Show", command = self.show_graph)

        self.menu_choose_machine.grid(row=1, column=1)
        self.menu_choose_x.grid(row=1, column=2)
        self.menu_choose_y.grid(row=1, column=3)
        self.button_show_graph.grid(row=1, column=4)

        self.frame_options.pack(side=tk.TOP)

        self.graph = None

    def check_x_to_y(self, selection):
        """
        Keep options compatible
        """

        pass

    def check_y_to_x(self, selection):
        """
        Keep options compatible
        """

        pass
    
    def update_graph(self):
        if self.graph is not None:  self.graph.update_graph()

    def show_graph(self):
        self.is_shown = not(self.is_shown)        
        if self.is_shown is True:
            self.graph = Graph(self, self.main_application, self.recipient.get(), self.x.get(), self.y.get())
            self.graph.pack(side=tk.BOTTOM)
        else:
            self.graph.destroy()
            self.graph = None