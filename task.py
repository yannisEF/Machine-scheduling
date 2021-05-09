class Task:
    """
    A task which lengths are sampled from probability distributions
    """
    id = 0
    def __init__(self, distrib):
        self.currentStep = 0

        self.realLength, self.error, self.arrivalTime = distrib.sample()
        self.predLength = self.realLength + self.error

        # paused, working, finished, notAvailable
        self.status = "notAvailable"
        
        self.paused = False

        self.finished = False
        self.timeFinished = None

        self.id = Task.id
        Task.id += 1
    
    def forward(self, step=1):
        """
        Execute the task, returns if the task is finished or not
        """
        if self.paused is True:
            raise RuntimeError("Task {} is paused/notAvailable and cannot run.".format(self.id))
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
    
    def restart(self):
        """
        Restarts the task
        """
        self.status = "notAvailable"
        self.paused = True
        self.finished = False
        self.timeFinished = None
        self.isAvailable = False
        self.currentStep = 0

    def __str__(self):
        return "Task {}   \t arrival time : {}   \t real length : {}   \t predicted length : {}   \t remaining : {}   \t status : {}".format(self.id, self.arrivalTime, self.realLength, self.predLength, round(self.realLength - self.currentStep,2), self.status)