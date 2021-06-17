import tkinter as tk
import tkinter.messagebox as mbox

from copy import deepcopy
from task import Task
from utils import reset_entry

class TaskManager(tk.LabelFrame):
    """
    Allows to add new tasks to machine
    """

    default_add = 5

    def __init__(self, master, main_application, distribution):
        super().__init__(master, text="Add new tasks")
        self.master = master
        self.main_application = main_application

        self.distribution = distribution
        self.recipient = tk.StringVar()

        # Frame containing the sending buttons and recipient
        self.frame_send = tk.Frame(self)

        self.available_machines = ["All machines"] + ["{} {}".format(m.name, m.id) for m in self.main_application.machines]
        self.machine_chosen = None
        self.menu_choose_machine = tk.OptionMenu(self.frame_send, self.recipient, *self.available_machines, command=self.set_machine_chosen)
        self.button_send = tk.Button(self.frame_send, text="Add tasks", command=self.add_tasks)
        self.button_clear = tk.Button(self.frame_send, text="Clear tasks", command=self.clear_tasks)

        self.menu_choose_machine.grid(row=0, column=1)
        self.button_send.grid(row=0, column=2)
        self.button_clear.grid(row=0, column=3)

        self.frame_send.pack(side=tk.TOP)

        # Frame containing the distribution's parameters
        self.frame_parameters = tk.LabelFrame(self, text="Tasks parameters")

        self.frame_number = tk.LabelFrame(self.frame_parameters, text="Number of tasks")
        self.entry_number = tk.Entry(self.frame_number)

        self.button_reset_params = tk.Button(self.frame_parameters, text="Reset", command=self.reset_params)

        self.frame_distrib_length = tk.LabelFrame(self.frame_parameters, text="Real length parameters")
        self.entries_length = [tk.Entry(self.frame_distrib_length) for _ in range(len(self.distribution.params[0]))]
        self.labels_length = [tk.Label(self.frame_distrib_length, text=list(
            self.distribution.params[0])[k] + ' :') for k in range(len(self.distribution.params[0]))]

        self.frame_distrib_error = tk.LabelFrame(self.frame_parameters, text="Prediction parameters")
        self.entries_error = [tk.Entry(self.frame_distrib_error) for _ in range(len(self.distribution.params[1]))]
        self.labels_error = [tk.Label(self.frame_distrib_error, text=list(
            self.distribution.params[1])[k]+ ' :') for k in range(len(self.distribution.params[1]))]

        self.frame_distrib_arrival = tk.LabelFrame(self.frame_parameters, text="Arrival time parameters")
        self.entries_arrival = [tk.Entry(self.frame_distrib_arrival) for _ in range(len(self.distribution.params[2]))]
        self.labels_arrival = [tk.Label(self.frame_distrib_arrival, text=list(
            self.distribution.params[2])[k] + ' :') for k in range(len(self.distribution.params[2]))]

        self.is_arrival = tk.IntVar(value=1)
        self.check_arrival = tk.Checkbutton(self.frame_distrib_arrival, variable=self.is_arrival,
                                            onvalue=1, offvalue=0, text="Enable arrival time", command=self.arrival_checked)

        self.entry_number.insert(tk.END, TaskManager.default_add)
        self.entry_number.pack()
        self.frame_number.grid(row=1, column=0)

        self.button_reset_params.grid(row=1, column=1)

        self.frame_distrib_length.grid(row=2)
        for k in range(len(self.entries_length)):
            self.labels_length[k].grid(row=k, column=0)
            self.entries_length[k].insert(tk.END, list(self.distribution.params[0].values())[k])
            self.entries_length[k].grid(row=k, column=1)

        self.frame_distrib_error.grid(row=3)
        for k in range(len(self.entries_error)):
            self.labels_error[k].grid(row=k, column=0)
            self.entries_error[k].insert(tk.END, list(self.distribution.params[1].values())[k])
            self.entries_error[k].grid(row=k, column=1)

        self.frame_distrib_arrival.grid(row=4)
        for k in range(len(self.entries_arrival)):
            self.labels_arrival[k].grid(row=k+1, column=0)
            self.entries_arrival[k].insert(tk.END, list(self.distribution.params[2].values())[k])
            self.entries_arrival[k].grid(row=k+1, column=1)
        self.check_arrival.grid(row=0)

        self.frame_parameters.pack(side=tk.BOTTOM)

    def reset_params(self):
        reset_entry(self.entry_number, TaskManager.default_add)

        for k in range(len(self.entries_length)):
            reset_entry(self.entries_length[k], list(self.distribution.params[0].values())[k])

        for k in range(len(self.entries_error)):
            reset_entry(self.entries_error[k], list(self.distribution.params[1].values())[k])

        for k in range(len(self.entries_arrival)):
            reset_entry(self.entries_arrival[k], list(self.distribution.params[2].values())[k])

    def arrival_checked(self):
        for entry in self.entries_arrival:
            entry.configure(state="normal" if self.is_arrival.get() == 1 else "disable")

    def set_machine_chosen(self, selection):
        self.machine_chosen = selection

    def add_tasks(self):
        new_distribution = deepcopy(self.distribution)

        try:
            for k in range(len(self.entries_length)):
                new_value = float(self.entries_length[k].get())
                new_distribution.params[0][list(new_distribution.params[0])[k]] = new_value

            for k in range(len(self.entries_error)):
                new_value = float(self.entries_error[k].get())
                new_distribution.params[1][list(new_distribution.params[1])[k]] = new_value

            if self.is_arrival.get() == 1:
                for k in range(len(self.entries_arrival)):
                    new_value = float(self.entries_arrival[k].get())
                    new_distribution.params[2][list(new_distribution.params[2])[k]] = new_value
            else:
                new_distribution.func[2] = None
                new_distribution.params[2] = None

            machines = self.main_application.name_to_machine[self.machine_chosen]
            if type(machines) is not list: machines = [machines]
            for _ in range(int(self.entry_number.get())):
                for m in machines:  self.main_application.add_task(m, Task(new_distribution, m.currentTime))

        except ValueError:
            mbox.showinfo(title="Value Error", message="Please enter a correct value.")
        except KeyError:
            mbox.showinfo(title="Key Error", message="Please choose a machine.")

    def clear_tasks(self):
        try:
            machines = self.main_application.name_to_machine[self.machine_chosen]
            if type(machines) is not list: machines = [machines]
            for m in machines:
                for task in list(m.allTasks.values()):
                    self.main_application.remove_task(m, task)

        except KeyError:
            mbox.showinfo(title="Key Error", message="Please choose a machine.")
