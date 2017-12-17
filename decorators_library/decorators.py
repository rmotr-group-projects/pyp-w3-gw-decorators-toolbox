from decorators_library.exceptions import FunctionTimeoutException
import signal
import time
import logging


def inspect(orig_fn):
    def wrapper(*args, **kwargs):
        if len(kwargs) == 0:
            print("{} invoked with {}, {}. Result: {}".format(orig_fn.__name__, args[0], args[1], orig_fn(*args)))
        else:
            print("{} invoked with {}, {}, operation={}. Result: {}".format(orig_fn.__name__, args[0], args[1], kwargs['operation'], orig_fn(*args, **kwargs)))
        return orig_fn(*args, **kwargs)
    return wrapper
    
class timeout(object):
    def __init__(self, time, exception = FunctionTimeoutException):
        self.time = time
        self.exception = exception
        
    def __call__(self, orig_fn):
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, self.raise_exception)
            signal.alarm(self.time)
            result = orig_fn(*args, **kwargs)
            signal.alarm(0)     #disable the alarm
            return result
        return wrapper
        
    def raise_exception(self, signum, stack):
        raise self.exception("Function call timed out")
        
def debug(logger = None):
    def dec(orig_fn):
        def wrapper(*args, **kwargs):
            if logger == None:
                print('Executing "{}" with params: {}, {}'.format(orig_fn.__name__, args, kwargs))
                print('Finished "{}" execution with result: {}'.format(orig_fn.__name__, orig_fn(*args, **kwargs)))
                return orig_fn(*args, **kwargs)
            else:
                return orig_fn(*args, **kwargs)
        return wrapper
    return dec
    
class memoized(object):
    def __init__(self, orig_fn):
        self.orig_fn = orig_fn
        self.cache = {}
 
    def __call__(self, *args):
        for key in self.cache.keys(): 
            if key == args: 
                return self.cache[key] 
        self.cache[args] = self.orig_fn(*args)
        return self.cache[args]

class count_calls(object):
    count = {}
    def __init__(self, orig_fn):
        self.orig_fn = orig_fn
        self.count[self.orig_fn.__name__] = 0
    
    def __call__(self, *args, **kwargs):
        self.count[self.orig_fn.__name__] += 1
        return self.orig_fn(*args, **kwargs)

    def counter(self):
        return self.count[self.orig_fn.__name__]
    
    @classmethod    
    def counters(cls):
        return cls.count
        
    @classmethod    
    def reset_counters(cls):
        cls.count = {}
        
def count_calls2(orig_fn):
    def wrapper(*args, **kwargs):
        wrapper.counter += 1
        return orig_fn(*args, **kwargs)
    wrapper.counter = 0
    wrapper.__name__ = orig_fn.__name__
    return wrapper
