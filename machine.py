import random

from distribution import Distribution
from task import Task
from utils import clearPrint


class Machine:
    """
    A machine that can work on tasks
    """
    id = 0
    def __init__(self, speed=1, key=lambda t: t.id, name="Machine"):
        self.id = Machine.id
        Machine.id += 1
        self.name = name

        self.allTasks = {}
        self.workingTasks = {}
        self.pausedTasks = {}
        self.finishedTasks = {}
        self.unavailableTasks = {}

        # The machine's execution speed
        self.speed = speed

        # The time of the machine
        self.currentTime = 0

        # A key to sort tasks in plot
        self.key = key

        # A progress bar
        self.progressBar = None

        # Average wait time, starts at 0
        self.average_wait_time = 0

    def addTask(self, newTask):
        """
        Adds a task to the set of all tasks
        """
        if newTask not in self.allTasks.values():
            self.allTasks[newTask.id] = newTask
            if newTask.status == "unavailable":
                self.unavailableTasks[newTask.id] = newTask
            else:
                self.pausedTasks[newTask.id] = newTask

    def removeTask(self, otherTask):
        """
        Removes a task from all sets of the machine
        """
        def removeFromDic(A, x):
            try:
                del A[x]
            except KeyError:
                pass

        otherTask = otherTask if type(otherTask) is int else otherTask.id
        removeFromDic(self.allTasks, otherTask)
        removeFromDic(self.workingTasks, otherTask)
        removeFromDic(self.pausedTasks, otherTask)
        removeFromDic(self.finishedTasks, otherTask)            
        removeFromDic(self.finishedTasks, otherTask)   

    def startTask(self, newTask):
        """
        Adds a task to the working set
        """
        newTask.status = "working"
        newTask.paused = False
        self.workingTasks[newTask.id] = newTask
        try:
            del self.pausedTasks[newTask.id]
        except KeyError:
            pass
    
    def makeAvailable(self, newTask):
        """
        Makes a task available
        """
        newTask.status = "paused"
        newTask.paused = True
        self.pausedTasks[newTask.id] = newTask
        try:
            del self.unavailableTasks[newTask.id]
        except KeyError:
            pass

    def stopTask(self, task):
        """
        Remove a task from the working set
        """
        del self.workingTasks[task.id]

    def pauseTask(self, task):
        """
        Pause a task in the working set
        """
        task.status = "paused"
        task.paused = True
        self.pausedTasks[task.id] = task
        self.stopTask(task)
    
    def finishTask(self, task):
        """
        Adds a task to the set of finished tasks
        """
        task.status = "finished"
        task.timeFinished = self.currentTime

        self.finishedTasks[task.id] = task
        n = len(self.finishedTasks)
        self.average_wait_time *= (n-1) / n
        self.average_wait_time += self.currentTime / n
        # not right time, maybe mistake in forward
        
        self.stopTask(task)
    
    def work(self, step):
        """
        Work on a step of the machine
        """
        nextStep = step * self.speed
        self.currentTime += step

        toMakeAvailable = []
        for task in self.unavailableTasks.values():
            if self.currentTime >= task.arrivalTime:
                toMakeAvailable.append(task)
        
        for task in toMakeAvailable:
            self.makeAvailable(task)

        toFinish = []
        for task in self.workingTasks.values():
            if task.forward(nextStep) is True:
                toFinish.append(task)
        
        for task in toFinish:
            if self.progressBar is not None:    self.progressBar.next()
            self.finishTask(task)

        return bool(self)
    
    def run(self, step):
        """
        Abstract run method, terminates when all tasks are finished
        """
        return False
    
    def boot(self, step, show=True, progressBar=None):
        """
        Boot the machine and runs it until every task is finished
        """
        doPrint = show is True and progressBar is None
        self.progressBar = progressBar

        if doPrint is True:    clearPrint(self)
        while self.run(step) is not True:
            if doPrint is True:    clearPrint(self)
        if doPrint is True:    clearPrint(self)

    def __bool__(self):
        """
        Returns if all tasks are finished
        """
        return len(self.finishedTasks) == len(self.allTasks)

    def __str__(self):
        total, working, paused, finished = len(self.allTasks), len(self.workingTasks), len(self.pausedTasks), len(self.finishedTasks)
        text = "Machine {} \t total : {} \t working : {} \t paused : {} \t finished : {} \t current time : {}\n".format(self.id, total, working, paused, finished, round(self.currentTime,2))

        for task in sorted(self.allTasks.values(), key=self.key):
            text += "\n\t" + str(task)

        return text + '\n'

    def __len__(self):
        return len(self.allTasks)

if __name__ == "__main__":
    from distribution import distrib

    tasks = [Task(distrib) for _ in range(38)]

    m = Machine()
    for task in tasks:
        m.addTask(task)

    print(m)
    input()
    m.key = lambda t: t.arrivalTime
    print(m)