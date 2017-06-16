# implement your decorators here.
import time
import logging
from .exceptions import *

def timeout(runtime):
    def timeout_dec(function):
        def newfunction(*args):
            clock = time.time()
            res = function(*args)
            end = time.time()
            # if timeit.timeit(function(*args), number = 1) <= time:
            if end-clock <= runtime:
                return res
            else:
                raise TimeoutError("Function call timed out")
        return newfunction
    return timeout_dec


class debug(object):
    def __init__(self, logger = None):
        if logger is None:
            self.loggertype = logging.getLogger('tests.test_decorators')
            self.loggertype.setLevel(logging.DEBUG)
        else:
            self.loggertype = logger
            
    def __call__(self, func):
        def debug_internal(*args):
            self.loggertype.debug('Executing "%s" with params: %s, {}' % (func.__name__, args))
            r = func(*args)
            self.loggertype.debug('Finished "{}" execution with result: {}'.format(func.__name__, r))
            return r
        return debug_internal

# One count_calls method
# class count_calls():
#     number_of_calls = {}
    
#     def __init__(self, func):
#         self.func = func
#         count_calls.number_of_calls[self.func.__name__] = 0
#         # learned that you can reference a class within itself
        
#     def __call__(self, *args, **kwargs):
#         count_calls.number_of_calls[self.func.__name__] += 1
#         return self.func(*args, **kwargs)
        
#     @classmethod
#     def reset_counters(cls):
#         cls.number_of_calls = {}
        
#     @classmethod
#     def counters(cls):
#         return cls.number_of_calls
    
#     def counter(self):
#         return count_calls.number_of_calls[self.func.__name__]
#     # func.counter() = int
        
        
#Another count_calls method
class count_calls():
    trackdict = {}
    def __init__(self, func):
        self.func = func
        self.counter = lambda: count_calls.trackdict[self.func.__name__] 
        self.counters = lambda: {self.func.__name__:count_calls.trackdict[self.func.__name__]}
        # self.reset_counters = lambda: dict.fromkeys(count_calls.trackdict, 0)
        count_calls.trackdict[self.func.__name__] = 0
        
    def __call__(self, *args, **kwargs):
        count_calls.trackdict[self.func.__name__] += 1
        return self.func(*args, **kwargs)
    @classmethod
    def counters(cls):
        return cls.trackdict
    @classmethod
    def reset_counters(cls):
        cls.trackdict = {}


class memoized():
    def __init__(self, func):
        self.func = func
        self.cache = {}
        
    def __call__(self, *args):
        if args in self.cache.keys():
            return self.cache[args]
        else:
            self.cache[args] = self.func(*args)
            return self.func(*args)
            
# def timing(runtime):
#     def timing_dec(function):
#         def origfunction(*args, **kwarg)
