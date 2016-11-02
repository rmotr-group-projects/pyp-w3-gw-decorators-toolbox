import logging 
import sys

#debug
def debug(logger=None):
    
    def log_function(original_function):
        # 
        logger = logging.getLogger(original_function.__module__)
        logger.setLevel(logging.DEBUG)
        
        def wrapper(*args, **kwargs):
            if logger != 'error_logger':
                
                logger.debug('Executing \"%s\" with params: %s, %s', original_function.__name__, args, kwargs)
                logger.debug('Finished \"%s\" execution with result: %s', original_function.__name__, original_function(*args))
            
            return original_function(*args, **kwargs)
        
        return wrapper
        
    return log_function

#@debug(logger='error_logger')
@debug()
def my_add(a, b):
    return a + b

my_add(1,2)

#timeout

#count_calls as a class

#memoize as a method?