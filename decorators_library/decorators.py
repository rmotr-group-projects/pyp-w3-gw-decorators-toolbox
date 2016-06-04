# implement your decorators here.
#import signal
import time
import logging
from exceptions import TimeoutError
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
        
def debug():
    def finished_func(func):
        def _new_func(*args, **kwargs):
            logging.debug('Executing {} with {}, {}'.format(func, *args, **kwargs))
            return func(*args, **kwargs)
        logging.debug('Finished {} executed with result: {}'.format(func, _new_func))
    return finished_func
    
# def memoized():
#     pass


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
#     print('didnt werk')
    
# func()