import logging
import signal
import time
from .exceptions import TimeoutError
import datetime
import math

# implement your decorators here.

# functionhistory = {}

# def memoized(fn):
#     def new_f(a,b):
#         if str(a+b) in functionhistory.keys():
#             return functionhistory[(str(a+b))]
#         else:
#             functionhistory[str(a+b)] = fn(a,b)
#             return fn(a,b)
#     return new_f    



class memoized(object):
    def __init__(self, f):
        self.f = f
        self.cache = {}   
    
    def __call__(self, *args):
        if args in self.cache.keys():
            return self.cache[args]
        else:
            self.cache[args] = self.f(*args)
            return self.cache[args]
    
        
        
class count_calls(object):
    
    functioncount = {}
    
    def __init__(self, f):
        self.f = f
        count_calls.functioncount[self.f.__name__] = 0 
        

    def __call__(self, *args):
        count_calls.functioncount[self.f.__name__] += 1
        return self.f(*args)

    @classmethod
    def reset_counters(cls):
        cls.functioncount = {}
    
    @classmethod
    def counters(cls):
        
        return cls.functioncount
    
    def counter(self):
        return count_calls.functioncount[self.f.__name__]
        
        
class debug(object):
    def __init__(self, logger=None):
        self.logger = logger

    
    def __call__(self, f):
        if not self.logger:
            self.logger = logging.getLogger(f.__module__)
        def innerfunction(*args, **kwargs):
        
            self.logger.debug('Executing "{}" with params: {}, {}'.format(f.__name__, args, kwargs))
            result = f(*args, **kwargs)
            self.logger.debug('Finished "{}" execution with result: {}'.format(f.__name__, result))
            
            return result
        return innerfunction
    



class timeout(object):
    def __init__(self, timeoutvalue):
        self.timeoutvalue = timeoutvalue
    
    def _handle_timeout(self,signum,frame):
        raise TimeoutError('Function call timed out')
    
    def __call__(self, f):
        def innerfunction(*args, **kwargs):
        
            signal.signal(signal.SIGALRM, self._handle_timeout)
            signal.alarm(self.timeoutvalue)
        
            try:
                result = f(*args,**kwargs)
            finally:
                signal.alarm(0)
            return result
        return innerfunction    

       
def funtimer(f):
    def innerfunction(*args,**kwargs):
        start_time = time.time()
        result = f(*args,**kwargs)
        end_time = time.time()
        runtime = math.ceil(end_time - start_time)
        logger = logging.getLogger(f.__module__)
        logger.debug('Function took {} to run'.format(runtime))
        return result
    return innerfunction
    
        

            
class timelastran(object):
    
    timecounter = {}
    
    def __init__(self, f):
        self.f = f
        timelastran.timecounter[self.f.__name__] = time.strftime(("%Y-%m-%d %H:%M:%S"))
        

    def __call__(self, *args):
        timelastran.timecounter[self.f.__name__] = time.strftime(("%Y-%m-%d %H:%M:%S"))
        return self.f(*args)
        
    def lasttime(self):
        return timelastran.timecounter[self.f.__name__]