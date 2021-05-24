
from task import Task
from machine import Machine

class Prediction(Machine):
    """
    Prediction algorithm, executes the tasks one by one, shortest predicted length increasing
    """
    def __init__(self, speed=1, key=lambda t: t.id, name="Prediction"):
        Machine.__init__(self, speed, key, name) 
    
    def run(self, step, timeCoef=1):
        if len(self.workingTasks) == 0 and len(self.pausedTasks) != 0:
            nextTask = sorted(list(self.pausedTasks.values()), key=lambda x:x.predLength)[0]
            self.startTask(nextTask)
        return self.work(step,timeCoef=timeCoef)

if __name__ == "__main__":
    from distribution import distrib

    tasks = [Task(distrib) for _ in range(3)]

    m = Prediction(key=lambda t: t.realLength)

    for task in tasks:
        m.addTask(task)

    m.boot(1)

    for task in tasks:
        print(task.timeFinished)