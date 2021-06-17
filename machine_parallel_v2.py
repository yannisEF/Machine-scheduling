import numpy as np

from machine_parallel import Parallel

class Parallel_v2(Parallel):
    """
    Prediction + Round-Robin, dynamic lambda parameter
    """
    def __init__(self, speed=1, lmb=.5, key=lambda x: x.id, coef=np.log(2)/2):
        super().__init__(speed, lmb, key)
        self.name = "PAR_DYN"
        
        self.historyLmb = [lmb]
        self.coef = coef

    def updateLmb(self):
        if len(self.finishedTasks) != 0 and len(self.finishedTasks) % 5 == 0:
            meanDiff = np.mean([abs(task.currentStep - task.predLength) for task in self.finishedTasks.values()])
            newLmb = np.exp(-meanDiff*self.coef)

            self.prediction.speed = self.speed * newLmb
            self.roundRobin.initSpeed = self.speed * (1-newLmb)
            self.historyLmb.append(newLmb)

    def finishTasks(self):
        super().finishTasks()
        self.updateLmb()

if __name__ == "__main__":
    from distribution import distrib
    from task import Task

    tasks = [Task(distrib) for _ in range(50)]

    m = Parallel_v2()

    for task in tasks:
        m.addTask(task)

    m.boot(1)