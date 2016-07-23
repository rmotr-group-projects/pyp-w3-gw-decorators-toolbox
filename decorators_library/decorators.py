import time
import logging
from timeit import Timer
import signal
from testfixtures import LogCapture
from decorators_library.exceptions import *

#decorators-library


def timeout(val):
    def gen(orig_f):      
        def handle_timeout(signum, frame):
            raise TimeoutError('Function call timed out')
        
        def run_w_time():
            signal.signal(signal.SIGALRM, handle_timeout)
            signal.alarm(val)
            orig_f()
            signal.alarm(0)
        return run_w_time
    return gen
        

class count_calls(object):
    
    function_dict = {}
    
    def __init__(self, func):
        self.func = func
        self.invocations = 0
        count_calls.function_dict[func] = self
        
    def __call__(self, *args, **kwargs):
        self.invocations += 1
        count_calls.function_dict[self.func].invocations = self.invocations
        return self.func(*args, **kwargs)
    
    def counter(self):
        return count_calls.function_dict[self.func].invocations
    
    #returns dictionary of all functions and their # called 
    @classmethod
    def counters(cls):
        result_dict = {}
        for f in cls.function_dict:
            result_dict[f.__name__] = cls.function_dict[f].invocations
        return result_dict
           
           
    @classmethod
    def reset_counters(cls):
        cls.function_dict = {}
           
           
class memoized(object):
    def __init__(self, func, *args):
        self.function = func
        self.cache = {}
        
    def __call__(self, *args):
        if args in self.cache:
            return self.cache[args]
        else:
            result = self.function(*args)
            self.cache[args]= result
            return result
            

class debug(object):
    def __init__(self, logger=None):
        self.logger = logger
        
    def __call__(self, function, *args, **kargs):
        if self.logger:
            result_log = self.logger
        else:
            result_log = logging.getLogger(function.__module__)
            logging.basicConfig()
            result_log.setLevel(logging.DEBUG)
        
        def dec(*args, **kwargs):
            result_log.debug('Executing \"{}\" with params: {}, {}'.format(function.__name__,args, kargs))
            temp_result = function(*args, **kargs)
            result_log.debug('Finished \"{}\" execution with result: {}'.format(function.__name__, temp_result))
            return temp_result
        return dec

        
        
           
          