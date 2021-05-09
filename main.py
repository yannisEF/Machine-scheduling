import random
import copy
import numpy as np
import matplotlib.pyplot as plt

from distribution import *
from task import Task

from slowBar import SlowBar

from machine_spt import ShortestProcessingTime
from machine_prediction import Prediction
from machine_round_robin import RoundRobin
from machine_parallel import Parallel
from machine_parallel_v2 import Parallel_v2

from distribution import getDistrib

random.seed(1)

def run(distrib, *machines, nTasks=50, nRun=1):
    meanSum = []
    with SlowBar("Running every machine on {} tasks for {} runs".format(nTasks,nRun), max=nRun*nTasks) as bar:
            for i in range(nRun):
                tasks = [Task(distrib) for _ in range(nTasks)]
                #for t in tasks[:5]:
                #    print(str(t))
                for k in range(len(machines)):
                    m = machines[k]
                    tasksList = [copy.deepcopy(tasks) for _ in machines]
                    for task in tasksList[k]:
                        m.addTask(task)
                    m.boot(1, show=False, progressBar=bar)   
                mSum = []
                for m in machines:
                    endTimes = [round(t.timeFinished) for t in m.finishedTasks.values()]
                    mSum.append(sum(endTimes)/len(endTimes))
                meanSum.append(mSum)
    meanSum = np.mean(meanSum, axis=0)
    return meanSum


def test0():
    nTasks, nRun, distrib = 50, 10, Distribution(distrib3, {'a':1,'b':20}, distrib2, {'mu':(1+20)/2, 'sigma':.5}, distrib3, {'a':1,'b':600})
    meanSum, meanLmb = [], []
    with SlowBar("Running every machine on {} tasks for {} runs".format(nTasks,nRun), max=nRun*nTasks) as bar:
        for i in range(nRun):
            m1 = ShortestProcessingTime(key=lambda t: t.realLength)
            m2 = Prediction(key=lambda t: t.realLength)
            m3 = RoundRobin(key=lambda t: t.realLength)
            pm = Parallel(lmb=.5)
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
    plt.xlabel('Time')
    plt.ylabel('Value of lambda')
    plt.legend('The evolution of lambda with respect to Time')
    plt.savefig('fig0')
    plt.show()


def test1():
    '''
    Prediction and RR
    '''
    L2 = list(np.arange(0.1, 2, 0.05))
    res = np.zeros((len(L2), 2))
    for j in range(len(L2)):
        noice_sigma = L2[j]
        distrib = Distribution(distrib3, {'a':1,'b':20}, distrib2, {'mu':(1+20)/2, 'sigma':noice_sigma}, distrib3, {'a':1,'b':600})
        m1 = Prediction(key=lambda t: t.realLength)
        m2 = RoundRobin(key=lambda t: t.realLength)
        res[j] = run(distrib, m1, m2)
    
    plt.figure()
    plt.plot(L2,res[:,0], 'r', label = 'Pred')
    plt.plot(L2,res[:,1], 'b', label = 'RR')
    plt.xlabel('Noice_Sigma')
    plt.ylabel('Completion Time')
    plt.legend()
    plt.savefig('fig1')
    plt.show()

    return res

def test2():
    '''
    Parallel machine 1 vs Parallel machine 2
    '''
    initLambda = list(np.arange(0.1, 1.1, 0.1))
    res = np.zeros((len(initLambda), 2))

    distrib = Distribution(distrib3, {'a':1,'b':20}, distrib2, {'mu':(1+20)/2, 'sigma':.5}, distrib3, {'a':1,'b':600})

    for i in range(len(initLambda)):
        lambd = initLambda[i]
        m1 = Parallel(lmb= lambd)
        m2 = Parallel_v2()
        res[i] = run(distrib, m1, m2)
    
    plt.figure()
    plt.plot(initLambda,res[:,0], 'r', label = 'P1')
    plt.plot(initLambda,res[:,1], 'b', label = 'P2')
    plt.xlabel('init Lambda')
    plt.ylabel('Completion Time')
    plt.legend()
    plt.savefig('fig2')
    plt.show()    

    return res


def test3():
    meanSum = []
    L2 = list(np.arange(0.1, 2, 0.05))
    res = np.zeros((len(L2), 4))
    for j in range(len(L2)):
        noice_sigma = L2[j]
        distrib = Distribution(distrib3, {'a':1,'b':20}, distrib2, {'mu':(1+20)/2, 'sigma':noice_sigma}, distrib3, {'a':1,'b':600})
        m1 = ShortestProcessingTime(key=lambda t: t.realLength)
        m2 = Prediction(key=lambda t: t.realLength)
        m3 = RoundRobin(key=lambda t: t.realLength)
        pm = Parallel(lmb=.5)
        res[j] = run(distrib, m1, m2, m3, pm)


    plt.figure(figsize=(10,10))
    plt.plot(L2,res[:,0], 'r', label = 'SPT')
    plt.plot(L2,res[:,1], 'y', label = 'Pred')
    plt.plot(L2,res[:,2], 'b', label = 'RR')
    plt.plot(L2,res[:,3], 'g', label = 'Parallel')
    plt.xlabel('Noice_Sigma')
    plt.ylabel('Completion Time')
    plt.legend()
    plt.savefig('fig3')
    plt.show()

    return res




if __name__ == "__main__":
    test0()
    res1 = test1()
    res2 = test2()
    res3 = test3()