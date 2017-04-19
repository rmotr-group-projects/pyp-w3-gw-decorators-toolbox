from .exceptions import *
import signal, os, time
from functools import wraps
import logging

#call handler when time limit has exceeded
def timeout(time):#passing parameter to decorator
    def decorate(func):#actual decorator 
        @wraps(func)
        def handler(signum, frame):
            raise TimeoutError('Function call timed out')
            #handler's purpose to raise error, stop execution
        def func_wrapper(*args):
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(time)
            try:
                return func(*args) 
            finally:
                signal.alarm(0) # disables
                 # instance of correct object/method
        
        return func_wrapper #returns for new_f
    return decorate # each method should return themselves after being run




class debug(object):
        
    def __init__(self, logger=None):
        self.logger = logger
    
    def __call__(self, func):
        
        def func_wrapper(*args, **kwargs):
            if not self.logger:
                logging.basicConfig()
                self.logger = logging.getLogger(func.__module__)
	        #logging.basicConfig(format='%(messages)s', level=logging.DEBUG)
	        #like that
	        # it passed for both?
            result = func(*args, **kwargs)
            self.logger.debug('Executing "{}" with params: {}, {{}}'.format(func.__name__, args, kwargs))
            self.logger.debug('Finished "{}" execution with result: {}'.format(func.__name__, result))
            return result
        return func_wrapper    
            #logging.basicConfig(format='%(func.__module__)s %(messages)s', level=logging.DEBUG)
            
    
            
            

    
class count_calls(object): 
    d = {} # create a dict to store methods and values 
    
    def __init__(self, func): #
        self.func = func #initialize self
        count_calls.d[func.__name__] = 0 #adding value to object name 
        
    def __call__(self, *args): 
        count_calls.d[self.func.__name__] += 1 #adding func + value to d
        self.func(*args) # returning value
        
    def counter(self):
        return count_calls.d[self.func.__name__] #calling the dictionary value for that method
    
    @classmethod #must be the whole class to reset all
    def reset_counters(cls):
       cls.d = {} # empty 
       return cls.d 

    @classmethod
    def counters(cls):
        return cls.d  # returns counter dict
    
    
class memoized(object):   
    cache = {}
    
    def __init__(self, func):
        self.func = func
        
    def __call__(self, *args):
        self.cache[args] = self.func(*args) # args = key / value = result
        return self.func(*args)
        
    
