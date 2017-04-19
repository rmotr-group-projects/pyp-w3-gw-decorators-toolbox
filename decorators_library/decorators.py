import time
from exceptions import TimeoutError

def timeout(func):
    
    
    def f(num):
        time = time.clock()
        while time != num:
            time = time.clock()
            return func(num)
        else:
            raise TimeoutError("Function call timed out")




def debug():
    pass
    """
    print("Executing '{}' with params: '{}'".format(func.__name__, func.__args__))
    """



class count_calls(object):
    """
    Returns a function. Tracks the number of times that it was called.
    """
    
    # dict of decorated functions and their counts.
    all_counters = {}
    
    def __init__(self, func):
        
        self.calls = 0
        self.func = func
        self.all_counters.update({self.func.__name__: self.calls})

    # when function is called, update the dictionary.
    def __call__(self, *args, **kwargs):
        self.calls += 1
        self.all_counters.update({self.func.__name__: self.calls})
        return self.func(*args, **kwargs)


    def counter(self):
        return self.calls
    
    @classmethod
    def counters(cls):
        return cls.all_counters
        
    @classmethod
    def reset_counters(cls):
        
        cls.all_counters = {}
    

class memoized(object):
    """
    Returns a function. Caprutes .
    """

    def __init__(self, f):
        self.f = f
        self.cache = {} # {(1, 2): 3, (2, 3): 5}

    def __call__(self, *args):
        self.f(*args)
        if not isinstance(args, tuple):
            raise Exception
        if not args in self.cache:
            total = args[0] + args[1]
            self.cache.update({args: total})
            return self.cache[args]
        return self.cache[args]
        
