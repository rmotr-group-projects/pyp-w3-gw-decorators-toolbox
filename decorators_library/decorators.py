import time
from functools import wraps
import signal
import logging 

from decorators_library.exceptions import FunctionTimeoutException

def inspect(org_func):
    def wrapped(*args, **kwargs):
        org_r = org_func(*args, **kwargs)
        org_func_name = org_func.__name__
        if len(kwargs) > 0: 
            print("{} invoked with {}, {}, operation={}. Result: {}".format(org_func_name, args[0], args[1], kwargs['operation'], org_r))
        else: 
            print("{} invoked with {}, {}. Result: {}".format(org_func_name, args[0], args[1], org_r))
        return org_r
    return wrapped

# @inspect
# def my_add(a, b):
#     return a + b

# print(my_add(a=3, b=5))  # 8
# Printed: "my_add invoked with 3, 5. Result: 8"




def timeout_old(time_limit, exception = FunctionTimeoutException, error_message='Function call timed out'):
    def real_decorator(org_fun):
        @wraps(org_fun)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            org_fun(*args, **kwargs)
            elapsed_time = time.time() + start_time
            if elapsed_time > time_limit:
                raise FunctionTimeoutException(error_message)
            return 
        return wrapper
    return real_decorator

# reference: https://pymotw.com/2/signal/
class timeout(object):
    def __init__(self, time_limit, exception=FunctionTimeoutException):
        self.time_limit = time_limit 
        self.exception = exception 
        
    def receive_alarm(self, signum, stack):
        raise self.exception("Function call timed out")
    
    def __call__(self, org_func):
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, self.receive_alarm)
            signal.alarm(self.time_limit)
            org_r = org_func(*args, **kwargs)
            signal.alarm(0)
            return org_r 
        return wrapper 

# @timeout(1)
# def very_slow_function():
#     time.sleep(2)
# very_slow_function()
# FunctionTimeoutException: Function call timed out

# class MyVeryCoolException(Exception):
#     pass

# @timeout(1, exception=MyVeryCoolException, error_message='????')
# def very_slow_function():
#     time.sleep(2)

# very_slow_function()





# reference: https://pymotw.com/3/logging/
class debug(object):
    def __init__(self, logger=None):
        self.logger = logger 
    
    def __call__(self, org_func):
        def wrapper(*args, **kwargs): 
            org_func_name = org_func.__name__
            org_r = org_func(*args, **kwargs)
            if self.logger is None: 
                self.logger = logging.getLogger(org_func.__module__)
            self.logger.debug('Executing "{}" with params: {}, {}'.format(org_func_name, args, kwargs))
            self.logger.debug('Finished "{}" execution with result: {}'.format(org_func_name, org_r))
            return org_r
        return wrapper 

# @debug()
# def my_add(a, b):
#     return a + b

# my_add(1, 2)
# Executing "my_add" with params: (1, 2), {}
# Finished "my_add" execution with result: 3



class count_calls(object): 
    function_count = {}
    
    def __init__(self, org_fun):
        self.org_fun = org_fun 
        self.function_count[self.org_fun.__name__] = 0
        
    def __call__(self, *args, **kwargs):
        self.function_count[self.org_fun.__name__] += 1 
        return self.org_fun(*args, **kwargs) 
    
    def counter(self): 
        return self.function_count[self.org_fun.__name__]
        
    @classmethod
    def counters(cls):
        return cls.function_count 
    
    @classmethod 
    def reset_counters(cls):
        cls.function_count = {} 

# @count_calls
# def my_func():
#   pass

# my_func()
# my_func()
# my_func()
# my_func()
# print(my_func.counter())
# 4



class memoized(object):

    def __init__(self, org_fun):
        self.org_fun = org_fun
        self.cache = {}

    def __call__(self, *args):
        if args in self.cache:
            return self.cache[args]
        else:
            value = self.org_fun(*args)
            self.cache[args] = value
            return value

# @memoized
# def add(a, b):
#     return a + b

# print(add(1, 2))
#3
# print(add(2, 3))
# 5
# print(add(1, 2))
# 3  # `add` was not executed, result was returned from internal cache