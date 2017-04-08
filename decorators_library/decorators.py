import time
import signal
from .exceptions import *
import logging
import functools
from collections import defaultdict
import random


# implement your decorators here.
def catcher(signum, _):
    raise TimeoutError('Function call timed out')
        
        
def timeout(takeout_time):
    def wrapper(func):
        def my_func(*args, **kwargs):
            signal.signal(signal.SIGALRM, catcher)
            signal.setitimer(signal.ITIMER_REAL, 2)
            return func(*args, **kwargs)
        return my_func
    return wrapper
    #    keep running the function
    # other:
    #   raise timeout exception


class debug(object):
    
    def __init__(self, logger=None):
        self.l = logger

    '''
    This decorator is suppose to debug the executions of the decorated 
    function by logging a message before starting the execution including given 
    params, and a second message after the execution is finished with the returned 
    result.
    '''
    def __call__(self, func):
        if not self.l:
            logging.basicConfig()
            self.l = logging.getLogger(func.__module__)
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            self.l.debug('Executing "{}" with params: {}, {}'.format(func.__name__, args, kwargs))
            result = func(*args, **kwargs)
            self.l.debug('Finished "{}" execution with result: {}'.format(func.__name__, result))
            return result
        return wrapper    
    
    
        
        # ('tests.test_decorators', 'DEBUG', 'Executing "my_add" with params: (1, 2), {}'),
        # ('tests.test_decorators', 'DEBUG', 'Finished "my_add" execution with result: 3')
    
    


class count_calls():
    functions_called = defaultdict(int)
    def __init__(self, function):
        self.function = function
    
        
    def __call__(self, *args, **kwargs):
        count_calls.functions_called[self.function.__name__] += 1
        return self.function(*args, **kwargs)
        
    
    def counter(self):
        return count_calls.functions_called[self.function.__name__]
    
    @classmethod
    def counters(cls):
        #self.assertEqual(count_calls.counters(), {'my_func': 0})
        # return
        return cls.functions_called
    
    @classmethod
    def reset_counters(cls):
        cls.functions_called = defaultdict(int)




class memoized():
    def __init__(self, function):
        self.cache = {}
        self.function = function
    
    def __call__(self, *args):
        if args in self.cache:
            return self.cache[args]
        else:
            result = self.function(*args)
            self.cache[args] = result
            return result
    

def add_one_to_inputs(func):
    ''' adds one to the function inputs... Why?
        Thats up to you!
    '''
    def wrapper(x, y):
        return func(x+1, y+1)
    return wrapper
    
    
def randomize_inputs(func):
    def wrapper(x, y):
        rand_x = random.randint(2, 10) * x
        rand_y = random.randint(2, 10) * y
        return func(rand_x, rand_y)
    return wrapper
# my_func(1, 2, 3, other=4, stuff=5)
# args = (1, 2, 3)
# kwargs = {'other': 4, 'stuff': 5}
# *args 1, 2, 3
# **kwargs other=4, stuff=5
# args = {
    
# my_func(1, 2, 3
# 6
# @memoize
# def my_func(*args):
#     return sum(args)

# cache {}
# cache {(1, 2, 3): 6}