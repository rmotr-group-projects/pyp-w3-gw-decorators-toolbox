import time
import logging
from functools import wraps
from decorators_library.exceptions import *


def timeout(time_limit):
    def dec(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            if end - start > time_limit:
                raise TimeoutError("Function call timed out")
            else:    
                return result
                
        return wrapper
        
    return dec


# Original code. Substituted with ideas from python cookbook

# def timeout(f, provided_time, *args, **kwargs):
#     t1 = time()
#     result = f(args, args)
#     elapsed_t = time() - t1
#     if elapsed_t > provided_time:
#         raise Exception("Function call timed out")
#     else:
#         return result


def debug(logger=None):

    if not logger: #make a logger if there isnt one
            logger = logging.getLogger(__name__)
            
    def decorate(func):
    
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.debug('Executing "{}" with params: {}, {}'.format(func.__name__, args, kwargs))
            result = func(*args, **kwargs)
            logger.debug('Finished "{}" execution with result: {}'.format(func.__name__, result))
            return result
        return wrapper
    return decorate

#replaced original code to use logger and to add layer per python cookbook
# def debug(func, *args, **kwargs):
#     print('Executing "{}" with params: "{}, {}"'.format(func.__name__, args, kwargs))
#     result = func(*args, **kwargs)
#     print('Finished "{}" execution with result: {}'.format(func.__name__, result))
#     return result

class count_calls(object):
    
    #count = 0
    count_dict = {}
    
    def __init__(self, f, *args, **kwargs):
        #self.count = 0
        self.funct = f
        if not f.__name__ in count_calls.count_dict:
            count_calls.count_dict[f.__name__] = 0
    
    
    def __call__(self, *args, **kwargs):
        result = self.funct(*args, **kwargs)
        count_calls.count_dict[self.funct.__name__] += 1
        return result

    @classmethod    
    def counters(cls):
        #return {self.funct :  self.count}
        return count_calls.count_dict
        
    def counter(self):
        if self.funct.__name__ in count_calls.count_dict:
            return count_calls.count_dict[self.funct.__name__]
        else:
            return 0
        
    
    @classmethod    
    def reset_counters(cls):
        count_calls.count_dict = {}



class memoized(object):
    def __init__(self, f, *args):
        self.cache = {} #empty dict
        self.func = f

    def __call__(self, *args):
        if args not in self.cache:
            result = self.func(*args)
            self.cache[args] = result
            return result
        else:
           return self.cache[args]
           
        


def check_arg_type(func, *args):
    def decorated(*args):
        types = [type(arg) for arg in args]
        print("Arguments types are {}".format(types))
        return func(*args)
    return decorated
        


def lowercaseArguments(f, *args):
    def decorated(*args):
        args = tuple([arg.lower() for arg in args if type(arg) is str])
        return f(*args)
    return decorated
    