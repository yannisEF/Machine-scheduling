import tkinter as tk

from machine_spt import ShortestProcessingTime
from machine_prediction import Prediction
from machine_round_robin import RoundRobin

from utils import randomTasks
from canvas import Canvas
from timeline import Timeline


class MainApplication(tk.Frame):

    min_speed, max_speed = 1, 5
    base_speed = 1000

    def __init__(self, master):
        super().__init__(master)

        self.speed = 1
        self.is_paused = True

        self.machines = []
        for _ in range(10):
            self.machines.append(Prediction())
            for task in randomTasks(1, 10):
                self.machines[-1].addTask(task)

        self.canvas = Canvas(self, self.machines)
        self.timeline = Timeline(self)

        self.pack()
    
    def change_speed(self, new_speed):
        if new_speed < MainApplication.min_speed:   new_speed = MainApplication.min_speed
        elif new_speed > MainApplication.max_speed: new_speed = MainApplication.max_speed

        self.speed = round(new_speed)

    def run(self):
        self.canvas.run(None)

    def _check_run(self):
        """
        If application is not paused, runs a step
        """
        if self.is_paused is False:
            self.run()
            self.after(int(MainApplication.base_speed/self.speed), self._check_run)

    def change_pause(self):
        self.is_paused = not(self.is_paused)
        self._check_run()
    
    
if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root)
    root.mainloop()