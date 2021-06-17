import tkinter as tk

from utils import reset_entry

class Timeline(tk.LabelFrame):
    """
    Allows to speed up and pause application
    """

    parameters = {}

    speed_sensitivity = 2

    def __init__(self, master, main_application):
        super().__init__(master, text="Play menu")
        self.master = master
        self.main_application = main_application

        # Speed label
        self.label_speed = tk.Label(self, text=self.main_application.speed)
        self.label_speed.grid(row=0, column=2)

        # Speed buttons
        self.frame_button = tk.Frame(self)

        self.button_decrease_speed = tk.Button(self.frame_button, text="<<", command=lambda: self.increment_speed(-1))
        self.button_decrease_speed.grid(row=1, column=1)

        self.button_pause = tk.Button(self.frame_button, text="Play", command=self.play_and_pause)
        self.button_pause.grid(row=1, column=2)

        self.button_increase_speed = tk.Button(self.frame_button, text=">>", command=lambda: self.increment_speed(1))
        self.button_increase_speed.grid(row=1, column=3)

        self.frame_button.grid(row=1,column=2)

        # Speed entry
        self.entry_speed = tk.Entry(self)
        self.entry_speed.bind("<Return>", self.set_speed)

        self.entry_speed.grid(row=2, column=2)        
  
    def update_speed_text(self):
        self.label_speed['text'] = str(round(self.main_application.speed/Timeline.speed_sensitivity))

    def increment_speed(self, direction):
        self.main_application.change_speed(self.main_application.speed + direction * Timeline.speed_sensitivity)
        self.update_speed_text()

    def play_and_pause(self):
        self.main_application.change_pause()
        self.button_pause['text'] = "Play" if self.main_application.is_paused is True else "Pause"
        self.update_speed_text()

    def set_speed(self, event):
        try:
            self.main_application.change_speed(float(self.entry_speed.get()))
        except ValueError:  pass

        reset_entry(self.entry_speed)
        self.update_speed_text()