import signal
import time
import logging
from .exceptions import FunctionTimeoutException

class timeout(object):
    def __init__(self, value, exception=FunctionTimeoutException):
        self.value = value
        self.exception = exception

       
    def __call__(self, func):
        def wrapped(*args, **kwargs):
            def alarm(signum, stack):
                raise FunctionTimeoutException('Function call timed out')
             
            signal.signal(signal.SIGALRM, alarm)
            signal.alarm(self.value)
            
            return func(*args, **kwargs)
        return wrapped
        
        
class memoized(object):
    def __init__(self, func):
        self.func = func
        self.cache = {}   
    
    def __call__(self, *args):
        if args in self.cache.keys():
            return self.cache[args]
        else:
            self.cache[args] = self.func(*args)
            return self.cache[args]
            
            
class count_calls(object):
    func_count = {}
    
    def __init__(self, func):
        self.func = func
        self.func_count[func.__name__] = 0
        
    def __call__(self, *args, **kwargs):
        count_calls.func_count[self.func.__name__] += 1
        return self.func(*args, **kwargs)
        
    def counter(self):
        return count_calls.func_count[self.func.__name__]
        
    @classmethod
    def counters(cls):
        return cls.func_count
        
    @classmethod
    def reset_counters(cls):
        cls.func_count.clear()


def inspect(func):
    def new_func(*args, **kwargs):
        
        text1 = "{} invoked with {}, {}"
        text2 = ", operation={}. Result: {}"
        text3 = ". Result: {}"
        
        res1 = text1.format(func.__name__, args[0], args[1])
        if (len(kwargs) > 0):
            res1 += text2.format(
                  kwargs['operation'], 
                  func(*args, **kwargs))
        else:   
            res1 += text3.format(func(*args))
    
        print(res1)
        return func(*args, **kwargs)
    return new_func
    

class debug(object):
    
    text1 = 'Executing "{}" with params: {}, {}'   
    text2 = 'Finished "{}" execution with result: {}'
    
    def __init__(self, logger=None):
        self.logger = logger
        
    def __call__(self, func):
        if not self.logger:
            self.logger = logging.getLogger(func.__module__)
        def logger_func(*args, **kwargs):
            self.logger.debug(self.text1.format(func.__name__, args, kwargs))
            result = func(*args, **kwargs)
            self.logger.debug(self.text2.format(func.__name__, result))
            
            return result
        return logger_func
        