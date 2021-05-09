
from task import Task
from machine import Machine

class RoundRobin(Machine):
    """
    Round-robin algorithm, executes all tasks equally at a reduced speed
    """
    def __init__(self, speed=1, key=lambda t: t.id, name="Round-Robin"):
        Machine.__init__(self, speed, key, name)
        self.initSpeed = speed

    def _initRun(self):
        L = list(self.pausedTasks.keys())
        for taskid in L:
            task = self.pausedTasks[taskid]
            self.startTask(task)
            
            
    def run(self, step):
        # if self.currentTime == 0:
        self._initRun()

        self.speed = self.initSpeed / max(1, len(self.workingTasks))
        return self.work(step)

if __name__ == "__main__":
    from distribution import distrib

    tasks = [Task(distrib) for _ in range(5)]

    m = RoundRobin(key=lambda t: t.realLength)

    for task in tasks:
        m.addTask(task)

    m.boot(1)