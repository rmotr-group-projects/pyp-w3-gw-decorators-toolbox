


def timeout():
    pass




def debug():
    pass


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
    

def memoized():
    pass


# implement your decorators here.

# @memoized
# def add(a, b):
#     return a + b
#     # add(1, 2)