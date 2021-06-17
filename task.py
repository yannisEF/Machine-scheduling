class Task:
    """
    A task which lengths are sampled from probability distributions
    """
    id = 0
    def __init__(self, distrib, init_time=0):
        self.currentStep = 0

        self.realLength, self.error, self.arrivalTime = distrib.sample()
        self.predLength = self.realLength + self.error
        self.arrivalTime += init_time

        # paused, working, finished
        self.status = "paused" if self.arrivalTime in (0, None) else "unavailable"
        self.paused = True

        self.finished = False
        self.timeFinished = None

        self.id = Task.id
        Task.id += 1
    
    def forward(self, step=1):
        """
        Execute the task, returns if the task is finished or not
        """
        if self.paused is True:
            raise RuntimeError("Task {} is {} and cannot run.".format(self.id, self.status))
        else:
            self.currentStep += step
            return self.hasFinished()
    
    def hasFinished(self):
        """
        Returns True if finished returns False if not
        """
        if self.currentStep >= self.realLength:
            self.timeFinished = self.currentStep
            self.finished = True

        return self.finished

    def __str__(self):
        if self.arrivalTime in (0, None):
            return "Task {}   \t real length : {}   \t predicted length : {}   \t remaining : {}   \t status : {}".format(
                self.id, self.realLength, self.predLength, round(self.realLength - self.currentStep, 2), self.status)
        return "Task {}   \t real length : {}   \t predicted length : {}   \t remaining : {}   \t arrival time : {} \t status : {}".format(
            self.id, self.realLength, self.predLength, round(self.realLength - self.currentStep, 2), self.arrivalTime, self.status)