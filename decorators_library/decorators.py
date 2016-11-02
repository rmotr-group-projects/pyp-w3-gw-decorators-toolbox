import logging 
import time
import signal
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
        
        """
        record start time
        run function
        record stop time
        
        time_to_run = stop_time - start_time
        

       if time_to_run > sec:
            raise TimeoutError('Function call timed out')
        """
"""
@timeout(1)
def my_add(a,b):
    time.sleep(2)
    return a + b
    
print(my_add(1,2))
"""


#count_calls as a class

#memoize as a method?