import time
import signal
from .exceptions import TimeoutError
from functools import wraps
import logging
# implement your decorators here.


class timeout(object):
    def __init__(self, timeout):
        self.timeout = timeout
        
    def _timeout_error(self, signum, frame):
        raise TimeoutError("Function call timed out")
        
    def __call__(self, function):
        def wrapper():
            signal.signal(signal.SIGALRM, self._timeout_error)
            signal.alarm(self.timeout)
            
            try:
                result = function()
            finally:
                signal.alarm(0)
        
        return wrapper
        

class debug(object):
    def __init__(self, logger=None):
        logging.basicConfig()
        self.logger = logger
        
    def __call__(self, function):
        def logging_function(*args, **kwargs):
            if self.logger is None:
                self.logger = logging.getLogger(function.__module__)
                self.logger.setLevel(logging.DEBUG)
            self.logger.debug('Executing "{0}" with params: {1}, {2}'.format(function.__name__,args,kwargs))
            return_value = function(*args,**kwargs)
            self.logger.debug('Finished "{0}" execution with result: {1}'.format(function.__name__,return_value))
            return return_value
        return logging_function

class count_calls(object):
    total = {}
    
    def __init__(self, function):
        self.function = function
        self.total[self.function.__name__] = 0 
        
    
    def __call__(self, *args, **kwargs):
        self.total[self.function.__name__] += 1
        return self.function(*args, **kwargs)
        
    def counter(self):
        return self.total[self.function.__name__]
        
    @classmethod
    def counters(cls):
        return cls.total
        
    @classmethod
    def reset_counters(cls):
        cls.total = {}
        
    
class memoized(object):
    def __init__(self, function):
        self.function = function
        self.cache = {}
        
    def __call__(self, *args, **kwargs):
        if args not in self.cache:
            self.cache[args] = self.function(*args, **kwargs)
            return self.function(*args)
        else:
            return self.cache[args]


'''
def run_time(function):
      
    def time(*args, **kwargs):
        start = time.time()
        result = function(*args, **kwargs)
        setattr(time, 'time_length', time.time() - start)
        return function(*args, **kwargs)
          
    return run_time
''' 
            

def timethis(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = function(*args, **kwargs)
        end = time.time()
        print(end-start)
        return result
    return wrapper

@timethis
def time_length(n):
  while n > 0:
    n -= 1 