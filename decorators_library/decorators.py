# implement your decorators here.
import time
import multiprocessing
from decorators_library.exceptions import *
import collections
import logging     


class timeout(object):
    
    def __init__(self, timelimit):
        self.timelimit = timelimit
        
    def __call__(self, func):
        
        def wrapper(*args, **kwargs):
            #process = process(function we want to time)
            process = multiprocessing.Process(target=func)
            process.start()
            
            process.join(self.timelimit)
            if process.is_alive():
                process.terminate()
                raise TimeoutError()

        return wrapper
  
  
class debug(object):

    def __init__(self, logger=None):
        self.logger = logger

        
    def __call__(self, func):
        def wrapper(*args, **kwargs):
            if self.logger is None:
                self.logger = logging.getLogger(func.__module__)
            name = func.__name__
            self.logger.debug('Executing "{}" with params: {}, {}'.format\
            (name, args, kwargs))
            result = func(*args, **kwargs)
            self.logger.debug('Finished "{}" execution with result: {}'\
            .format(name, result))
            return result
        return wrapper    


class count_calls(object):

    counter_dict = {}
    
    def __init__(self, func):
        self.func = func
        self.__class__.counter_dict[self.func.__name__] = 0
    
    def __call__(self, *args, **kwargs):
        self.__class__.counter_dict[self.func.__name__] += 1
        return self.func(*args, **kwargs)
        
    def counter(self):
        return self.__class__.counter_dict[self.func.__name__]
    
    @classmethod
    def counters(cls):
        return cls.counter_dict
        
    @classmethod
    def reset_counters(cls):
        cls.counter_dict = {}


class memoized(object):

    def __init__(self, func):
        self.func = func
        self.cache = {}
    
    def __call__(self, *args):
        if (args) in self.cache:
            return self.cache[(args)]
        else:
            result = self.func(*args)
            self.cache[(args)] = result
            return result
            
            
#creates a new int based on the numbers passed instead of 
#whatever behavior existed before, i.e., add(4, 6, 1) now returns 461
class concatenate:
    def __init__(self, *args):
        self.args = args
        
    
    def __call__(self, *args):
        for i in args:
            if not isinstance(i, (int)):
                raise TypeError('Argument supplied not of type int')
        result = int(''.join(map(str, args)))
        if result == 420:
            result = str(result) + ' blaze it'
        return result
        

#Converts int result of original function to binary string        
def binary_result(func):
    def wrapper(*args):
        result = func(*args)
        if not isinstance(result, (int)):
            raise TypeError('Result not of type int')
        return bin(result)
    return wrapper
    