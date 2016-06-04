import time
import logging

# from psutils import *
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
        
        result = self.func(*args, **kwargs)


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

    def decorate(func):
    
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.debug('Executing "{}" with params: "{}{}"'.format(func._, args, kwargs))
            result = func(*args, **kwargs)
            logger.debug('Finished "{}" execution with result: {}'.format(func.__name__, result))
            return result
        return wrapper
    return decorate

#replaced original code to use logger and to add layer per python cookbook
# def debug(func, *args, **kwargs):
#     print('Executing "{}" with params: "{}{}"'.format(func.__name__, args, kwargs))
#     result = func(*args, **kwargs)
#     print('Finished "{}" execution with result: {}'.format(func.__name__, result))
#     return result

class count_calls(object):
    
    count = 0
    
    def __init__(self, f, *args, **kwargs):
        self.count = 0
        self.funct = f
    
    def __call__(self, *args, **kwargs):
        result = self.funct(*args, **kwargs)
        self.count += 1
        return result
    
    def counter(self):
        return self.count
        
    def counters(self):
        return {self.funct :  self.count}
        
    def reset_counters(self):
        self.count = 0



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
           
        
#It was having trouble importing psutils
        
# def benchmarkRAM(f, *args, **kwargs):
#     initial_ram_usage = psutils.virtual_memory()
#     result = f(*args, **kwargs)
#     final_ram_usage = psutils.virtual_memory()
#     print("{} used {}bytes of memory".format(
#         f.__name__,
#         final_ram_usage.used - initial_ram_usage.used
#     ))


def check_arg_type(func, *args):
    types = [type(arg) for arg in args]
    print("Arguments types are {}".format(types))
    return func(*args)
        


def lowercaseArguments(f, *args):
    for arg in args:
        if type(arg) is str:
            arg = arg.lower()
    return f(*args)
    