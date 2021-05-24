
from task import Task
from utils import clearPrint
from machine_prediction import Prediction
from machine_round_robin import RoundRobin

from machine import Machine

class Parallel:
    """
    Prediction + Round-robin, runs the two algorithms in parallel at a speed lmb and 1-lmb
    """
    id = 0
    def __init__(self, speed=1, lmb=0.5, key=lambda x: x.id, name="Parallel"):
        self.name = name
        self.id = Parallel.id
        Parallel.id += 1

        self.speed = speed
        self.prediction = Prediction(speed * lmb, key)
        self.roundRobin = RoundRobin(speed * (1-lmb), key)

        self.currentStep = 0
        self.allTasks = {}
        self.finishedTasks = {}

    def reboot(self):
        self.prediction.reboot()
        self.roundRobin.reboot()
        self.currentStep = 0
        self.allTasks = {}
        self.finishedTasks = {}    

    def addTask(self, newTask):
        """
        Adds a task to the set of all tasks
        """
        self.prediction.addTask(newTask)
        self.roundRobin.addTask(newTask)
        self.allTasks[newTask.id] = newTask

    def removeTask(self, otherTask):
        """
        Removes a task from the machines
        """
        self.prediction.removeTask(otherTask)
        self.roundRobin.removeTask(otherTask)
        del self.allTasks[otherTask.id]
        try:
            del self.allTasks[otherTask.id]
        except KeyError:
            pass
    
    def finishTasks(self):
        for task in self.prediction.finishedTasks.values():
            #self.roundRobin.startTask(task)
            #self.roundRobin.finishTask(task)
            if task.finished:
                self.finishedTasks[task.id] = task
        for task in self.roundRobin.finishedTasks.values():
            #self.prediction.startTask(task)
            #self.prediction.finishTask(task)
            if task.finished:
                self.finishedTasks[task.id] = task


    def run(self, step):
        self.currentStep += step

        #self.startTasks()

        Machine.currentTime += step

        if not bool(self):
            self.prediction.run(step,timeCoef=0)
            self.roundRobin.run(step, timeCoef=0)

        self.finishTasks()

        return bool(self)

    def boot(self, step, show=True, progressBar=None):
        """
        Boot the machine and runs it until every task is finished
        """
        doPrint = show is True and progressBar is None

        if doPrint is True:    clearPrint(self)
        while self.run(step) is not True:
            if doPrint is True:    clearPrint(self)
            if progressBar is not None: progressBar.next()
        if doPrint is True:    clearPrint(self)

        Machine.currentTime = 0

    def __bool__(self):
        return bool(self.prediction) or bool(self.roundRobin)

    def __str__(self):
        text = "Parallel {} \t total : {} \t current step : {}\n".format(self.id, len(self.roundRobin.allTasks), self.currentStep)
        text += "\t" + self.prediction.name + str(self.prediction) + "\t speed : {}".format(self.prediction.speed) + '\n'
        text += "\t" + self.roundRobin.name + str(self.roundRobin) + "\t speed : {}".format(self.roundRobin.initSpeed) + '\n'
        return text

    def __len__(self):
        return len(self.allTasks)

if __name__ == "__main__":
    from distribution import distrib

    tasks = [Task(distrib) for _ in range(3)]

    m = Parallel()

    for task in tasks:
        m.addTask(task)

    m.boot(1)

    for task in tasks:
        print(task.timeFinished)

