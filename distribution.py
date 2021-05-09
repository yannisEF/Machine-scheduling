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
                
        #return (round(sampled), round(error))

def distrib1(*args, **kwargs):
    return random.expovariate(*args, **kwargs) + 1

def distrib2(*args, **kwargs):
    return random.normalvariate(*args, **kwargs)

def distrib3(a,b):
    return random.uniform(a,b)

#distrib = Distribution(distrib1, {'lambd':.5}, distrib2, {'mu':0, 'sigma':1.5}, distrib1, {'lambd':.5})
'''
def getDistrib(a1,b1, sigma, a, b):
    random.seed(1)
    return Distribution(distrib3, {'a':a1,'b':b1}, distrib2, {'mu':(a1+b1)/2, 'sigma':sigma}, distrib3, {'a':a,'b':b})
'''