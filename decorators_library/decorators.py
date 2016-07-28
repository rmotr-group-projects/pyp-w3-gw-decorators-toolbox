# implement your decorators here.
from time import sleep
import time
import signal
import logging

from decorators_library.exceptions import *

def timeout(max_time):
    '''Track the execution time and raise an exception if the time exceeds 
    given timeout range'''
    def decorate(func):
        def handler(signum, frame):
            raise TimeoutError()
            
        def new_f(*args, **kwargs):
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(max_time)
            
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result
        new_f.__name__ = func.__name__
        return new_f
    return decorate


class count_calls(object):
    '''Keeps track of how many times certain function was called'''
    collections_counter = {}
    
    def __init__(self, f):
        self.f = f
        self.__class__.collections_counter[f.__name__] = 0
        
    def __call__(self, *args, **kwargs):
        
        if self.f.__name__ in self.__class__.collections_counter:
            self.__class__.collections_counter[self.f.__name__] += 1
        else:
            self.__class__.collections_counter[self.f.__name__] = 1
        
    def counter(self):
        return self.__class__.collections_counter[self.f.__name__]

        
    @classmethod
    def counters(cls):
        return cls.collections_counter
        
    @classmethod
    def reset_counters(cls):
        cls.collections_counter = {}
        

class debug():
    '''Debug the executions of the decorated function by logging a message 
    before starting the execution including given params, and a second message 
    after the execution is finished with the returned result'''
    def __init__(self, logger=None):
        self.logger = logger
        
    def __call__(self, f):
        f_name = f.__name__
        
        def wrapper(*args, **kwargs):
            if self.logger is None:
                logging.basicConfig()
                self.logger = logging.getLogger(f.__module__)
            
            before = "Executing {}{}{} with params: {}, {}".format('"', f_name,'"', args, kwargs)
            result = f(*args, **kwargs)
            after = "Finished {}{}{} execution with result: {}".format('"', f_name,'"',result)

            self.logger.debug(before)
            self.logger.debug(after)
                      
            return result
        return wrapper

#py
class memoized(object):
    '''keep track of previous executions of the decorated function and the 
    result of the invokations. If the decorated function is execution again 
    using the same set of arguments sent in the past, the result must be 
    immediately returned by an internal cache instead of re executing the 
    same code again.'''
    def __init__(self, f):
        self.cache = {}
        self.f = f
    
    def __call__(self, *args):
        key = args
        if key in self.cache:
            return self.cache[key]
        else:
            result = self.f(*args)
            self.cache[key] = result
            return result
        
            
def run_time(func):
    '''Measures the total run time of a function '''
    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = func(*args, **kwargs)
        t2 = time.time() - t1
        return int(t2)
        
    return wrapper


def addDate(func):
    def newfunc(*arg, **kw):
        print("Today is {}. You are calling function \"{}\"".format(time.strftime("%d/%m/%Y"), func.__name__))
        print("You are on your way towards a great programmer")
        return func(*arg,**kw)
    return newfunc

def vectorize(func):
    '''Receives a list of elements and runs the function on each element'''
    def g(*args):
        return [func(el) for el in args]
    return g
