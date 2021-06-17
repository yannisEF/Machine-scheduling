import tkinter as tk

class Timeline(tk.Frame):
    parameters = {}

    speed_sensitivity = 1

    def __init__(self, master):
        super().__init__(master)
        self.master = master

        # Speed label
        self.label_speed = tk.Label(self, text=self.master.speed)
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

        self.grid(row=2, column=1)
    
    def update_speed_text(self):
        self.label_speed['text'] = str(self.master.speed)

    def increment_speed(self, direction):
        self.master.change_speed(self.master.speed + direction * Timeline.speed_sensitivity)
        self.update_speed_text()

    def play_and_pause(self):
        self.master.change_pause()
        self.button_pause['text'] = "Play" if self.master.is_paused is True else "Pause"
        self.update_speed_text()

    def set_speed(self, event):
        try:
            self.master.change_speed(float(self.entry_speed.get()))
        except ValueError:  pass

        self.entry_speed.delete(0, len(self.entry_speed.get()))
        self.update_speed_text()