import random
import numpy as np

class Distribution:
    """
    A probability distribution
    """
    def __init__(self, func1, params1, func2=None, params2=None, func3=lambda _=None:0, params3={}):
        self.params = (params1, params2, params3)
        self.func = (func1, func2, func3)

    def sample(self):
        sampled = self.func[0](**self.params[0])

        if self.func[1] is not None and self.params[1] is not None:
            error = -sampled
            while round(sampled) + round(error) <= 0:
                error = self.func[1](**self.params[1])
        
        arrival_time = self.func[2](**self.params[2])

        return (round(sampled), round(error), arrival_time)

# Length distribution
def distrib1(*args, **kwargs):
    return random.expovariate(*args, **kwargs) + 1

# Error of prediction distribution
def distrib2(*args, **kwargs):
    return random.normalvariate(*args, **kwargs)

# Arrival time distribution
def distrib3(*args, **kwargs):
    return round(np.random.poisson(size=1, **kwargs)[0])

distrib = Distribution(distrib1, {'lambd':.1}, distrib2, {'mu':0, 'sigma':4}, distrib3, {'lam':5})