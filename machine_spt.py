import random

from distribution import Distribution
from task import Task
from machine import Machine

class ShortestProcessingTime(Machine):
    """
    SPT algorithm, executes the tasks one by one, shortest real length increasing
    """
    def __init__(self, speed=1, key=lambda t: t.id):
        Machine.__init__(self, speed, key, name="SPT")
    
    def run(self, step):
        if len(self.pausedTasks) != 0 and len(self.workingTasks) == 0:
            nextTask = sorted(list(self.pausedTasks.values()), key=lambda x:x.realLength)[0]
            self.startTask(nextTask)
        return self.work(step)

if __name__ == "__main__":
    from distribution import distrib

    tasks = [Task(distrib) for _ in range(38)]

    m = ShortestProcessingTime(key=lambda t: t.realLength)

    for task in tasks:
        m.addTask(task)

    m.boot(1)