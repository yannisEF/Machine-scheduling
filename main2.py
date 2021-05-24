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

from scipy.interpolate import make_interp_spline, BSpline

random.seed(1)

def updateTaskNoises(tasks,distrib):
    for t in tasks:
        error = distrib.sample_error_only()
        t.predLength = t.realLength + error

def run(tasks, *machines, nRun=100, nTasks=100):
    meanSum = []
    #tasks = [Task(distrib) for _ in range(nTasks)]

    with SlowBar("Running every machine on {} tasks for {} runs".format(nTasks,nRun), max=nRun*nTasks) as bar:
            for i in range(nRun):

                for k in range(len(machines)):
                    m = machines[k]
                    tasksList = [copy.deepcopy(tasks) for _ in machines]
                    for task in tasksList[k]:
                        m.addTask(task)
                    m.boot(1, show=False, progressBar=bar)   
                mSum = []
                for m in machines:
                    endTimes = [round(t.timeFinished) for t in m.finishedTasks.values()]
                    #print(m,endTimes)
                    mSum.append(sum(endTimes)/len(endTimes))
                meanSum.append(mSum)

                for m in machines:
                    m.reboot()
                
                

    meanSum = np.mean(meanSum, axis=0)
    return meanSum


def test0(distrib):
    nTasks, nRun = 100, 5
    meanSum, meanLmb = [], []
    with SlowBar("Running every machine on {} tasks for {} runs".format(nTasks,nRun), max=nRun*nTasks) as bar:
        for i in range(nRun):
            m1 = ShortestProcessingTime(key=lambda t: t.realLength)
            m2 = Prediction(key=lambda t: t.realLength)
            m3 = RoundRobin(key=lambda t: t.realLength)
            pm = Parallel(lmb=0)
            pm2 = Parallel_v2(lmb=.1)
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
                #print(m,endTimes)
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


def test1(nTasks=500):
    '''
    Prediction according to noice
    '''
    
    L2 = list(np.arange(0.1, 2, 0.05))
    res = np.zeros((len(L2), 2))
    for j in range(len(L2)):
        noice_sigma = L2[j]
        distrib = Distribution(distrib3, {'alpha':1.1}, distrib2, {'mu':0, 'sigma':noice_sigma}, distrib2, {'mu':0, 'sigma':0})

        if j == 0:
            tasks = [Task(distrib) for _ in range(nTasks)]
        else:
            updateTaskNoises(tasks, distrib)

        m1 = Prediction(key=lambda t: t.realLength)
        #m2 = RoundRobin(key=lambda t: t.realLength)
        res[j] = run(tasks,m1)
        
    L2 = np.array(L2)
    x_smooth = np.linspace(L2.min(), L2.max(), 500)
    spl = make_interp_spline(L2, res[:,0])
    y_smooth1 = spl(x_smooth)
    plt.figure()
    plt.plot(x_smooth,y_smooth1, 'r', label = 'Pred')
    #plt.plot(L2,res[:,1], 'b', label = 'RR')
    plt.xlabel('Noice_Sigma')
    plt.ylabel('Completion Time')
    plt.legend()
    plt.savefig('fig_pred_noice')
    plt.show()

    return res

def test2(distrib,nTasks=50):
    '''
    Parallel machine 1 vs Parallel machine 2
    '''
    initLambda = list(np.arange(0.1, 1.1, 0.1))
    res = np.zeros((len(initLambda), 2))

    tasks = [Task(distrib) for _ in range(nTasks)]
    for i in range(len(initLambda)):
        lambd = initLambda[i]
        m1 = Parallel(lmb= lambd)
        m2 = Parallel_v2()
        res[i] = run(tasks, m1, m2)
    
    plt.figure()
    plt.plot(initLambda,res[:,0], 'r', label = 'Parallel')
    plt.plot(initLambda,res[:,1], 'b', label = 'Parallel_AutoLambda')
    plt.xlabel('init Lambda')
    plt.ylabel('Completion Time')
    plt.legend()
    plt.savefig('fig2')
    plt.show()    

    return res


def test3(nTasks=100):
    meanSum = []
    L2 = list(np.arange(1, 30, 5))
    res = np.zeros((len(L2), 5))

    lmb = 0.5

    for j in range(len(L2)):
        noice_sigma = L2[j]
        distrib = Distribution(distrib3, {'alpha':1.1}, distrib2, {'mu':0, 'sigma':noice_sigma}, distrib2, {'mu':0, 'sigma':0})

        if j==0:
            tasks = [Task(distrib) for _ in range(nTasks)]
        else:
            updateTaskNoises(tasks, distrib)

            if j == len(L2)/2:
                gen_tasks_stats(tasks)

        m1 = ShortestProcessingTime(key=lambda t: t.realLength)
        m2 = Prediction(key=lambda t: t.realLength)
        m3 = RoundRobin(key=lambda t: t.realLength)
        pm = Parallel_v2(lmb=0.5)
        pm2 = Parallel(lmb=lmb)
        res[j] = run(tasks, m1, m2, m3, pm, pm2)


    plt.figure(figsize=(8,8))
    plt.title('Evolution of Completion Time by Noise')
    plt.plot(L2,res[:,0], 'r', label = 'SPT')
    plt.plot(L2,res[:,1], 'y', label = 'Pred')
    plt.plot(L2,res[:,2], 'b', label = 'RR')
    plt.plot(L2,res[:,3], 'g', label = 'Parallel_AutoLambda')
    plt.plot(L2,res[:,4], 'm', label = 'Parallel_Lambda {}'.format(lmb))
    plt.xlabel('Noice_Sigma')
    plt.ylabel('Completion Time')
    plt.legend()
    plt.savefig('fig3')
    plt.show()

    plt.figure(figsize=(8,8))
    plt.title('Competitiveness Ratio Plot')
    plt.plot(L2,res[:,0]/res[:,0], 'r', label = 'SPT')
    plt.plot(L2,res[:,1]/res[:,0], 'y', label = 'Pred')
    plt.plot(L2,res[:,2]/res[:,0], 'b', label = 'RR')
    plt.plot(L2,res[:,3]/res[:,0], 'g', label = 'Parallel_AutoLambda')
    plt.plot(L2,res[:,4]/res[:,0], 'm', label = 'Parallel_Lambda {}'.format(lmb))
    plt.xlabel('Noice_Sigma')
    plt.ylabel('Competitiveness')
    plt.legend()
    plt.savefig('fig4')
    plt.show()    

    return res


def gen_tasks_stats(tasks):

    plt.figure(figsize=(8,8))
    plt.title('Histogram of Arrival Time')
    plt.hist([t.arrivalTime for t in tasks])
    plt.savefig('Histogram of Arrival Time')
    plt.show()

    plt.figure(figsize=(8,8))
    plt.title('Histogram of Real Length')
    plt.hist([t.realLength for t in tasks])
    plt.savefig('Histogram of Real Length')
    plt.show()    

    plt.figure(figsize=(8,8))
    plt.title('Histogram of Error')
    plt.hist([t.error for t in tasks])
    plt.savefig('Histogram of Error')
    plt.show()    


if __name__ == "__main__":
    #test0(distrib)
    
    #res1 = test1()
    #res2 = test2(distrib)
    res3 = test3()