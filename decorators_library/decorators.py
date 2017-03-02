import time
import multiprocessing.pool
import logging
from exceptions import TimeoutError


class timeout(object):
    
    def __init__(self, seconds):
        self.seconds = seconds
    
    def __call__(self, func):
        
        def wrapper(*args, **kwargs):
            pool = multiprocessing.pool.ThreadPool(processes=1)
            async_result = pool.apply_async(func, args, kwargs)
            
            try:
                return async_result.get(self.seconds)
            except:
                raise TimeoutError('Function call timed out')
            finally:
                pool.close()
            return func(*args, **kwargs)
            
        return wrapper


class debug(object):
    
    def __init__(self, logger=None):
            self.logger = logger
    
    def __call__(self, func):

        def wrapper(*args, **kwargs):
            if self.logger is None:
                self.logger = logging.getLogger(func.__module__)
                self.logger.setLevel(logging.DEBUG)
            self.logger.debug('Executing "{}" with params: {}, {}'.format(
                func.__name__, args, kwargs))
            result = func(*args, **kwargs)
            self.logger.debug('Finished "{}" execution with result: {}'.format(
                func.__name__, result))
            return result
            
        return wrapper
        

class count_calls(object):
    count_dict = {}
    
    def __init__(self, func):
        self.func = func
        self.func_name = func.__name__
        count_calls.count_dict[self.func_name] = 0
        
    def __call__(self, *args, **kwargs):
        count_calls.count_dict[self.func_name] += 1
        return self.func(*args, **kwargs)
        
    def counter(self):
        return count_calls.count_dict[self.func_name]
    
    @staticmethod
    def counters():
        return count_calls.count_dict
    
    @staticmethod    
    def reset_counters():
        count_calls.count_dict = {}


class memoized(object):
    
    def __init__(self, func):
        self.func = func
        self.cache = {}
        
    def __call__(self, *args):
        if args not in self.cache:
            self.cache[args] = self.func(*args)
        return self.cache[args]


class upper_case(object):
    """Makes returned string upper case.

    Can apply optional limit argument to shorten the number of characters the 
    string has. The string limit counter starts on the left of the string. 
    Returned value of original function must be a string"""
    
    def __init__(self, limit=None):
        self.limit = limit
        
    def __call__(self, func):
        
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            
            try:
                mod_result = result.upper()
            except:
                raise ValueError('Original function did not return a string.')
            
            if self.limit is None:
                return mod_result
            
            count = 0
            limit_result = ''
            for each in mod_result:
                if count < self.limit:
                    limit_result += each
                    count += 1
            return limit_result
            
        return wrapper
            

class no_spaces(object):
    """Replaces spaces in a string with '_'"""
    
    def __init__(self, func):
        self.func = func
    
    def __call__(self, *args, **kwargs):
        result = self.func(*args, **kwargs)
        mod_result = ""
        
        for letter in result:
            if letter == ' ':
                mod_result += '_'
            else:
                mod_result += letter
        
        return mod_result
                