# implement your decorators here.
#import signal
import time
import logging
from decorators_library.exceptions import *
from threading import Thread

# def timeout(seconds): # PROBLEMS: won't raise error
#     def wrapper(func):
#         def _new_func(*args, **kwargs):
#             try:
#                 func(*args, **kwargs)
#             except TimeoutError:
#                 raise 'Function call timed out'
#         timer = Thread(target=_new_func)
#         timer.daemon = True
#         try:
#             timer.start()
#             timer.join(seconds)
#         except TimeoutError:
#             raise TimeoutError('Function call timed out')
#         return _new_func
#     try:
#         return wrapper
#     except TimeoutError:
#         raise TimeoutError('Function call timed out')

def timeout(seconds):
    def actual_decorator(function):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            fast_enough = function(*args, **kwargs)
            end_time = time.time()
            print(end_time - start_time) #for debug purposes
            if end_time - start_time > seconds:
                raise TimeoutError('Function call timed out')
            else:
                return fast_enough
        return wrapper
    return actual_decorator
    
        
def debug(logger=None):
    def finished_func(func):
        if not logger:
            log = logging.getLogger(func.__module__)
            log.setLevel(logging.DEBUG)
        else:
            log = logger
        def _new_func(*args, **kwargs):
            arg_list = [x for x in args]
            log.debug('Executing \"{}\" with params: {}, {}'.format(func.__name__, tuple(arg_list), kwargs or '{}'))
            result = func(*args, **kwargs)
            log.debug('Finished \"{}\" execution with result: {}'.format(func.__name__, result))
            return result
        result = _new_func
        return result
    return finished_func
    
class memoized(object):
    def __init__(self, func):
        self.cache = {}
        self.func = func
        
    def __call__(self, *args):
        if args in self.cache:
            return self.cache[args]
        else:
            result = self.func(*args)
            self.cache.setdefault(args, result)
            return result

def count_calls(wrapped):
    def inner(*args, **kwargs):
        inner.count += 1
        return wrapped(*args, **kwargs)

    def counter():
        return inner.count

    def counters():
        return {k.__name__: v.count for k, v in count_calls.counter_dict.items()}

    def reset_counters():
        count_calls.counter_dict = {}

    inner.counter = counter
    count_calls.counters = counters
    count_calls.reset_counters = reset_counters

    if not hasattr(count_calls, 'counter_dict'):
        count_calls.counter_dict = {}
    count_calls.counter_dict[wrapped] = inner

    inner.count = 0
    return inner
    
    
# @timeout(1)    
# def func():
#     time.sleep(2)
#     print('didnt work :(')
    
