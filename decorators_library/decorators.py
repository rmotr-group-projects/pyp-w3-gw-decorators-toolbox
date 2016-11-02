from .exceptions import TimeoutError
import time
import logging

def timeout(integer):
    def decorator_function(func):
        def wrap(*args, **kwargs):
            begin = time.time()
            func(*args, **kwargs)
            end = time.time()
            
            if end - begin > integer:
                raise TimeoutError('Function call timed out')
                
        return wrap
    return decorator_function

def debug(logger = None):
    def decorator_function(func):
        def wrap(*args, **kwargs):
            result = func(*args, **kwargs)
            
            if logger:
                custom_logger = logger # logger argument is a logger object. no need to re-instantiate
                result = func(*args, **kwargs)
            else:
                custom_logger = logging.getLogger(func.__module__)
                custom_logger.debug('Executing "{}" with params: {}, {}'.format(func.__name__, args, kwargs))
                custom_logger.debug('Finished "{}" execution with result: {}'.format(func.__name__, result))
                
            return func(*args, **kwargs)
        return wrap
    return decorator_function
    
class count_calls:
    RUNNING_TOTALS = {}
    def __init__(self, func):
        self.func = func
        self.instance_count = 0
    
    def counter(self):
        self.RUNNING_TOTALS[self.func.__name__] = self.instance_count
        return self.instance_count
    
    @classmethod  
    def counters(self): # self is a class. we need the instance
        return self.RUNNING_TOTALS
    
    @classmethod   
    def reset_counters(self):
        self.RUNNING_TOTALS = {}
        
    def __call__(self,*args):
        self.instance_count += 1
        return self.func(*args)

class memoized(object):
    def __init__(self, func):
        self.func = func 
        self.cache = {}
    
    def __call__(self, *args):
        result = self.func(*args)
        self.cache[tuple(args)] = result
        
        return self.func(*args)