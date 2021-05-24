import random

class Distribution:
    """
    A probability distribution
    """
    def __init__(self, func1, params1, func2=None, params2=None, func3=None, param3=None):
        self.params = (params1, params2, param3)
        self.func = (func1, func2, func3)

    def sample(self):
        sampled = self.func[0](**self.params[0])

        if self.func[1] is not None and self.params[1] is not None:
            error = -sampled
            while round(sampled) + round(error) <= 0:
                error = self.func[1](**self.params[1])
            
            if self.func[2]: # generate random values for arrivalTime
                AT = self.func[2](**self.params[2])
            
        return (round(sampled), round(error), round(AT))
    
    def sample_error_only(self):
        return round(self.func[1](**self.params[1]))

def distrib1(*args, **kwargs):
    return random.expovariate(*args, **kwargs) + 1

def distrib2(*args, **kwargs):
    return random.normalvariate(*args, **kwargs)

def distrib3(*args, **kwargs):
    return (random.paretovariate(1.1) + 1)*3.


random.seed(1)
distrib = Distribution(distrib3, {}, distrib2, {'mu':0, 'sigma':1.5}, distrib1, {'lambd':.2})
