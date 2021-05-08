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

from distribution import distrib

random.seed()

m1 = ShortestProcessingTime(key=lambda t: t.realLength)
m2 = Prediction(key=lambda t: t.realLength)
m3 = RoundRobin(key=lambda t: t.realLength)
pm = Parallel(lmb=.9)
machines = [m1, m2, m3, pm]

tasks = [Task(distrib) for _ in range(100)]
tasksList = [copy.deepcopy(tasks) for _ in machines]

for k in range(len(machines)):
    m = machines[k]
    for task in tasksList[k]:
        m.addTask(task)
    with SlowBar("{} {}".format(m.name, m.id), max=len(m)) as bar:
        m.boot(1, show=False, progressBar=bar)

mSum = []
for m in machines:
    endTimes = [round(t.timeFinished) for t in m.finishedTasks.values()]
    mSum.append(sum(endTimes)/len(endTimes))

print(mSum)
plt.figure(figsize=(9,9))
plt.bar([m.name for m in machines], mSum)
plt.show()