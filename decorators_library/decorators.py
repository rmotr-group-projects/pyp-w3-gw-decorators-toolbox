# implement your decorators here.
from decorators_library.exceptions import FunctionTimeoutException
import signal
import logging 
def inspect(orig_func):
    def wrapped(*args, **kwargs):
        orig_res = orig_func(*args, **kwargs)
        func_name = orig_func.__name__
        if len(kwargs) > 0: 
            print("{} invoked with {}, {}, operation={}. Result: {}".format(func_name, args[0], args[1], kwargs['operation'], orig_res))
        else: 
            print("{} invoked with {}, {}. Result: {}".format(func_name, args[0], args[1], orig_res))
        return orig_res
    return wrapped
    

class timeout(object):
    def __init__(self, time, exception=FunctionTimeoutException):
        self.time = time 
        self.exception = exception 
        
    def raise_exception(self, signum, stack):
        raise self.exception("Function call timed out")
    
    def __call__(self, orig_func):
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, self.raise_exception)
            signal.alarm(self.time)
            orig_res = orig_func(*args, **kwargs)
            signal.alarm(0)
            return orig_res 
        return wrapper 


class count_calls(object): 
    total = {}
    def __init__(self, orig_func):
        self.orig_func = orig_func 
        self.total[self.orig_func.__name__] = 0
        
    def __call__(self, *args, **kwargs):
        self.total[self.orig_func.__name__] += 1 
        return self.orig_func(*args, **kwargs) 
    
    def counter(self): 
        return self.total[self.orig_func.__name__]
        
    @classmethod
    def counters(cls):
        return cls.total 
    
    @classmethod 
    def reset_counters(cls):
        cls.total = {} 
        

class memoized(object):
    
    def __init__(self, orig_func):
        self.orig_func = orig_func
        self.cache = {}
    
    def __call__(self, *args):
        for keys in self.cache.keys(): 
            if keys == args: 
                return self.cache[keys] 
        self.cache[args] = self.orig_func(*args)
        return self.cache[args]
    
class debug(object):
    def __init__(self, logger=None):
        self.logger = logger 
    
    def __call__(self, orig_func):
        def wrapper(*args, **kwargs): 
            func_name = orig_func.__name__
            orig_res = orig_func(*args, **kwargs)
            if self.logger is None: 
                self.logger = logging.getLogger(orig_func.__module__)
            self.logger.debug('Executing "{}" with params: {}, {}'.format(func_name, args, kwargs))
            self.logger.debug('Finished "{}" execution with result: {}'.format(func_name, orig_res))
            return orig_res
        return wrapper