import random

from distribution import Distribution
from task import Task
from utils import clearPrint
from machine_prediction import Prediction
from machine_round_robin import RoundRobin

class Parallel:
    """
    Prediction + Round-robin, runs the two algorithms in parallel at a speed lmb and 1-lmb
    """
    id = 0
    def __init__(self, speed=1, lmb=.5, key=lambda x: x.id, name="Parallel"):
        self.name = name
        self.id = Parallel.id
        Parallel.id += 1

        self.prediction = Prediction(speed * lmb, key)
        self.roundRobin = RoundRobin(speed * (1-lmb), key)

        self.contributionPrediction = 0
        self.contributionRoundRobin = 0

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

    def run(self, step):
        self.currentStep += step
        
        for task in self.prediction.finishedTasks.values():
            self.roundRobin.startTask(task)
            self.roundRobin.finishTask(task)
            if task.id not in self.finishedTasks.keys():
                self.contributionPrediction += 1
            self.finishedTasks[task.id] = task
        for task in self.roundRobin.finishedTasks.values():
            self.prediction.startTask(task)
            self.prediction.finishTask(task)
            if task.id not in self.finishedTasks.keys():
                self.contributionRoundRobin += 1
            self.finishedTasks[task.id] = task

        if not bool(self):
            self.prediction.run(step)
            self.roundRobin.run(step)

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

    def __bool__(self):
        return bool(self.prediction) or bool(self.roundRobin)

    def __str__(self):
        text = "Parallel {} \t total : {} \t current step : {}\t contribution Prediction {} \t contribution RoundRobin {}\n".format(self.id, len(self.roundRobin.allTasks), self.currentStep, self.contributionPrediction, self.contributionRoundRobin)
        text += "\t" + self.prediction.name + str(self.prediction)[7:str(self.prediction).find('current time')] + '\n'
        text += "\t" + self.roundRobin.name + str(self.roundRobin)[7:str(self.roundRobin).find('current time')] + '\n'
        return text

    def __len__(self):
        return len(self.allTasks)

if __name__ == "__main__":
    from distribution import distrib

    tasks = [Task(distrib) for _ in range(38)]

    m = Parallel()

    for task in tasks:
        m.addTask(task)

    m.boot(1)