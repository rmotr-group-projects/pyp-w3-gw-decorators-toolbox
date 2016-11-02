import logging 
import time
import signal
import functools
from .exceptions import *


#debug
def debug(logger=None):
    
    def log_function(original_function):

        def wrapper(*args, **kwargs):
            if logger is None:
                debug_logger = logging.getLogger(original_function.__module__)
                debug_logger.setLevel(logging.DEBUG)
                debug_logger.debug('Executing \"%s\" with params: %s, %s', original_function.__name__, args, kwargs)
                debug_logger.debug('Finished \"%s\" execution with result: %s', original_function.__name__, original_function(*args))
            
            return original_function(*args, **kwargs)
        
        return wrapper
        
    return log_function


#timeout
def timeout(sec=None):
    if sec is None:
        raise AttributeError('You need to provide a number of seconds.')
    else:
        
        def decorator(original_function):
            
            def raise_error(signum, frame):
                raise TimeoutError('Function call timed out')
                #print("ERROR")
            
            signal.signal(signal.SIGALRM, raise_error)
            signal.alarm(sec)
            
            def wrapper(*args, **kwargs):
                
                return original_function(*args, **kwargs)
            
            return wrapper
            
        signal.alarm(0)
    
        return decorator
        
#count_calls as a class
class count_calls(object):
    
    def __init__(self, function):
        self.count_dict = {}
        self.original_function = function
        self.f_name = self.original_function.__name__
    
    def __call__(self, *args, **kwargs):
        #print self.count_dict
        #print self.f_name
        #print self.count_dict.keys()
        
        if self.f_name in self.count_dict.keys():
            self.count_dict[self.f_name] += 1
        else:
            self.count_dict[self.f_name] = 1
        
        print self.count_dict
        
        return self.original_function(*args, **kwargs)
    
    def __get__(self, instance, instancetype):
        """Implement the descriptor protocol to make decorating instance 
        method possible.

        """
        return functools.partial(self.__call__, instance)
    
    def counter(self):
        return self.count_dict[self.f_name]
    
    @staticmethod
    def counters(self):
        return self.count_dict
        
    def reset_counters(self):
        self.count_dict = {}
 
class count_calls(object):
    count_dict = {}
    
    def __init__(self, function):
        self.original_function = function
        self.f_name = self.original_function.__name__
        self.count_dict[self.f_name] = 0
    
    def __call__(self, *args, **kwargs):
        #print self.count_dict
        #print self.f_name
        #print self.count_dict.keys()
        
        if self.f_name in self.count_dict.keys():
            self.count_dict[self.f_name] += 1
        else:
            self.count_dict[self.f_name] = 1
        
        print self.count_dict
        
        return self.original_function(*args, **kwargs)
    
    def counter(self):
        return self.count_dict[self.f_name]
    
    @classmethod
    def counters(self):
        return self.count_dict
    
    @classmethod
    def reset_counters(self):
        self.count_dict = {}
        
#memoize as a method?
