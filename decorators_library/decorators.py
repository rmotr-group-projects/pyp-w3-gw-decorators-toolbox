from decorators_library.exceptions import *
from functools import wraps
import signal 
import logging


def timeout(seconds=10, error_message='Function call timed out'):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator
    
def debug(logger=None):
    def decorate(func):
        log = logger if logger else logging.getLogger('tests.test_decorators')
        
        @wraps(func)  
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            log.debug('Executing "{}" with params: {}, {{}}'.format(func.__name__, args)) 
            log.debug('Finished "{}" execution with result: {}'.format(func.__name__, result))
            return result
        return wrapper
    return decorate
    
class count_calls(object):
    
    count = {}
    
    def __init__(self, func):
        self.func_name = func.__name__
        count_calls.count[self.func_name] = 0
        
    def __call__(self):
        count_calls.count[self.func_name] += 1
        self.func_name()
    
    def counter(self):
        return count_calls.count[self.func_name]
    
    @classmethod
    def counters(cls):
        return cls.count
    
    @classmethod
    def reset_counters(cls):
        cls.count = {}
    
    def __call__(self):
        self.count[self.func_name] += 1