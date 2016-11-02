import logging 
import sys

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

#count_calls as a class

#memoize as a method?