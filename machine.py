

from utils import clearPrint

class Machine:
    """
    A machine that can work on tasks
    """
    
    id = 0
    currentTime = 0
    def __init__(self, speed=1, key=lambda t: t.id, name="Machine"):
        self.id = Machine.id
        Machine.id += 1
        self.name = name

        self.allTasks = {}
        self.workingTasks = {}
        self.pausedTasks = {}
        self.notAvailableTasks = {}
        self.finishedTasks = {}

        # The machine's execution speed
        self.speed = speed

        # The time of the machine
        

        # A key to sort tasks in plot
        self.key = key

        # A progress bar
        self.progressBar = None
    
    def reboot(self):
        self.allTasks = {}
        self.workingTasks = {}
        self.pausedTasks = {}
        self.notAvailableTasks = {}
        self.finishedTasks = {}    
        Machine.currentTime = 0
        self.progressBar = None
    
    def addTask(self, newTask):
        """
        Adds a task to the set of all tasks
        """
        if newTask not in self.allTasks.values():
            self.allTasks[newTask.id] = newTask
            if newTask.arrivalTime == 0:
                self.pausedTasks[newTask.id] = newTask
            else:
                self.notAvailableTasks[newTask.id] = newTask

    def _removeFromDic(self, A, x):
        try:
            del A[x]
        except KeyError:
            pass

    def removeTask(self, otherTask):
        """
        Removes a task from all sets of the machine
        """

        otherTask = otherTask if type(otherTask) is int else otherTask.id
        self._removeFromDic(self.allTasks, otherTask)
        self._removeFromDic(self.workingTasks, otherTask)
        self._removeFromDic(self.pausedTasks, otherTask)
        self._removeFromDic(self.finishedTasks, otherTask)
        self._removeFromDic(self.notAvailableTasks, otherTask)            
        
    def startTask(self, newTask):
        """
        Adds a task to the working set
        if Machine.currentTime is less than newTask's arrivalTime, startTask fails
        """
        if Machine.currentTime < newTask.arrivalTime:
            raise RuntimeError("Machine.currentTime < arrivalTime")
        newTask.status = "working"
        newTask.paused = False
        self.workingTasks[newTask.id] = newTask
        try:
            del self.pausedTasks[newTask.id]
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
        if task.finished == True:
            
        #task.status = "finished"
        #task.timeFinished = Machine.currentTime

            self.finishedTasks[task.id] = task
            self.stopTask(task)
        
    def work(self, step, timeCoef=1):
        """
        Work on a step of the machine
        """
        nextStep = step * self.speed
        Machine.currentTime += step*timeCoef

        toFinish = []
        for task in self.workingTasks.values():
            if task.forward(nextStep) is True:
                toFinish.append(task)
        
        for task in toFinish:
            if self.progressBar is not None:    self.progressBar.next()
            self.finishTask(task)
        
        L = list(self.notAvailableTasks.keys())
        #for notAvailableTask in self.notAvailableTasks.values():
        for notAvailableTaskid in L:
            if notAvailableTaskid in self.pausedTasks:
                raise RuntimeError()
            notAvailableTask = self.notAvailableTasks[notAvailableTaskid]
            
            if Machine.currentTime >= notAvailableTask.arrivalTime:
                notAvailableTask.paused = True
                notAvailableTask.status = "paused"
                self.pausedTasks[notAvailableTask.id] = notAvailableTask
                self._removeFromDic(self.notAvailableTasks, notAvailableTaskid)

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

        Machine.currentTime = 0

    def __bool__(self):
        """
        Returns if all tasks are finished
        """
        return len(self.finishedTasks) == len(self.allTasks)

    def __str__(self):
        total, working, paused, finished = len(self.allTasks), len(self.workingTasks), len(self.pausedTasks), len(self.finishedTasks)
        text = "Machine {} \t total : {} \t working : {} \t paused : {} \t finished : {} \t current time : {}\n".format(self.id, total, working, paused, finished, round(Machine.currentTime,2))

        for task in sorted(self.allTasks.values(), key=self.key):
            text += "\n\t" + str(task)

        return text + '\n'

    def __len__(self):
        return len(self.allTasks)
