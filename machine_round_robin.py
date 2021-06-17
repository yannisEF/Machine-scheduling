import random

from distribution import Distribution
from task import Task
from machine import Machine

class RoundRobin(Machine):
    """
    Round-robin algorithm, executes all tasks equally at a reduced speed
    """
    def __init__(self, speed=1, key=lambda t: t.id):
        Machine.__init__(self, speed, key, name="RR")
        self.initSpeed = speed

    def _initRun(self):
        toStart = []
        for task in self.pausedTasks.values():
            toStart.append(task)
        
        for task in toStart:
            self.startTask(task)
            
    def run(self, step):
        self._initRun()

        if len(self.workingTasks) > 0:
            self.speed = self.initSpeed / len(self.workingTasks)
            return self.work(step)
        return self.work(step)

if __name__ == "__main__":
    from distribution import distrib

    tasks = [Task(distrib) for _ in range(38)]

    m = RoundRobin(key=lambda t: t.realLength)

    for task in tasks:
        m.addTask(task)

    m.boot(1)