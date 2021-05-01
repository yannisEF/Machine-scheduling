import random

class Distribution:
    """
    A probability distribution
    """
    def __init__(self, func1, params1, func2=None, params2=None):
        self.params = (params1, params2)
        self.func = (func1, func2)

    def sample(self):
        sampled = self.func[0](**self.params[0])

        if self.func[1] is not None and self.params[1] is not None:
            error = -sampled
            while round(sampled) + round(error) <= 0:
                error = self.func[1](**self.params[1])
        return (round(sampled), round(error))

def distrib1(*args, **kwargs):
    return random.expovariate(*args, **kwargs) + 1

def distrib2(*args, **kwargs):
    return random.normalvariate(*args, **kwargs)

distrib = Distribution(distrib1, {'lambd':.5}, distrib2, {'mu':0, 'sigma':1.5})