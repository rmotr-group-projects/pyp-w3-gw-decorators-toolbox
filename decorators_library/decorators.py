# implement your decorators here.
import time
from .exceptions import TimeoutError
import logging
import signal


def timeout(value):
    def outer_function(fn):
        def receive_alarm(signum, stack):
            raise TimeoutError("Function call timed out")

        signal.signal(signal.SIGALRM, receive_alarm)
        signal.alarm(value)
        return fn
    return outer_function


def debug(logger=None):
    if not logger:
        logging.basicConfig()
        logger = logging.getLogger('tests.test_decorators')
        logger.setLevel(logging.DEBUG)
    def out_func(fn):
        def inner_func(*args,**kwargs):
            logger.debug('Executing "{0}" with params: {1}, {2}'.format(fn.__name__, args, kwargs))
            logger.debug('Finished "{0}" execution with result: {1}'.format(fn.__name__, fn(*args,**kwargs)))
            return fn(*args,**kwargs)
        return inner_func
    return out_func

class count_calls(object):
    
    dict_counter = {}
    
    def __init__(self,fn):
        self.fn = fn
        self.count = 0
        self.dict_counter[self.fn.__name__] = self.count

        
    def __call__(self):
        self.count += 1
        self.dict_counter[self.fn.__name__] = self.count
        return self.fn
        
    def counter(self):
        return self.count
    
    @classmethod    
    def reset_counters(cls):
        cls.dict_counter = {}
        cls.count = 0
    
    @classmethod
    def counters(cls):
       return cls.dict_counter
       
       
class memoized(object):
    
    def __init__(self, fn):
        self.fn = fn
        self.cache = {}
        
    def __call__(self, *args, **kwargs):
        if args not in self.cache:
            result = self.fn(*args,**kwargs)
            self.cache[args] = result
            return self.fn(*args,**kwargs)
        else:
            return self.cache[args]
    
    
