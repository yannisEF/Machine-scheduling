import random
import copy
import numpy as np
import matplotlib.pyplot as plt

from distribution import Distribution
from task import Task

from slowBar import SlowBar

from machine_spt import ShortestProcessingTime
from machine_prediction import Prediction
from machine_round_robin import RoundRobin
from machine_parallel import Parallel
from machine_parallel_v2 import Parallel_v2

from distribution import distrib

random.seed()

nTasks, nRun = 100, 10
meanSum, meanLmb = [], []
with SlowBar("Running every machine on {} tasks for {} runs".format(nTasks,nRun), max=nRun*nTasks) as bar:
    for i in range(nRun):
        m1 = ShortestProcessingTime(key=lambda t: t.realLength)
        m2 = Prediction(key=lambda t: t.realLength)
        m3 = RoundRobin(key=lambda t: t.realLength)
        pm = Parallel(lmb=.9)
        pm2 = Parallel_v2(lmb=.5)
        machines = [m1, m2, m3, pm, pm2]

        tasks = [Task(distrib) for _ in range(nTasks)]
        tasksList = [copy.deepcopy(tasks) for _ in machines]

        for k in range(len(machines)):
            m = machines[k]
            for task in tasksList[k]:
                m.addTask(task)
            
            m.boot(1, show=False, progressBar=bar)

        # Autres métriques possibles
        mSum = []
        for m in machines:
            endTimes = [round(t.timeFinished) for t in m.finishedTasks.values()]
            mSum.append(sum(endTimes)/len(endTimes))

        meanSum.append(mSum)

        
        meanLmb.append(pm2.historyLmb)


meanSum = np.mean(meanSum, axis=0)

indLmb = [len(lmb) for lmb in meanLmb]
meanLmb = [[meanLmb[i][k] if k < indLmb[i] else 0 for k in range(max(indLmb))] for i in range(len(indLmb))]
meanLmb = np.mean(meanLmb, axis=0)

plt.figure(figsize=(9,9))
plt.bar([m.name for m in machines], meanSum)

plt.figure()
plt.plot(meanLmb)

plt.show()