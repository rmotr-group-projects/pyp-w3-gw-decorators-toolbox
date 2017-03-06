# implement your decorators here.
import time
import signal
import logging
from .exceptions import TimeoutError


       
        
class timeout(object):
    
    def __init__(self,allowed_time):
        self.allowed_time=allowed_time
        
    def _handle_timeout(self,signum, frame):
        raise TimeoutError("Function call timed out")
        
    def __call__(self,func):
        def wrapped():
            signal.signal(signal.SIGALRM,self._handle_timeout)
            signal.alarm(self.allowed_time)
            
            try:
                result=func()
            finally:
                signal.alarm(0)
        
        return wrapped
        
        
    
    
class debug(object):
    
    def __init__(self,logger=None):
        self.logger=logger
        
        
    def __call__(self,func):
        def wrapped(a,b):
            if self.logger is None:
                self.logger=logging.getLogger(func.__module__)
                self.logger.setLevel(logging.DEBUG)
            
            result=func(a,b)
            self.logger.debug('Executing "%s" with params: (%s, %s), {}', func.__name__, a, b)
            self.logger.debug('Finished "%s" execution with result: %s', func.__name__, result)
            return result                
        
        return wrapped
        

class count_calls(object):
    
    counterDict={}
    def __init__(self,func):
  
        self._count=0
        self.func=func
        count_calls.counterDict[self.func.__name__]=0
        
    def __call__(self):
        def wrapper():
            if self.func.__name__  in count_calls.counterDict.keys(): 
                self._count=count_calls.counterDict[self.func.__name__]
                self._count+=1
                count_calls.counterDict[self.func.__name__]=self._count

            return self.func
        return wrapper()
    
    
    def counter(self):
        return self._count
     
    @classmethod   
    def counters(self):
        return count_calls.counterDict
        
    @classmethod
    def reset_counters(self):
        count_calls.counterDict={}
        
class memoized(object):

    
    def __init__(self,func):
        self.cache={}
        self.func=func
        pass
    
    def __call__(self,a,b):

        if (a,b) in self.cache.keys():
            return self.cache[(a,b)]
        else:
            self.cache[(a,b)]=self.func(a,b)
           
        return self.func(a,b)
            
    
        
        
        
        
        
    
        
        