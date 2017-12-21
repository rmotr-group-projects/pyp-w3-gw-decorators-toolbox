from decorators_library.exceptions import FunctionTimeoutException
import functools
import time
import sys
import signal

# PYTHONPATH=. py.test -s tests/ -k


# class timeout(object):
#     def __init__(self, time_limit, exception=FunctionTimeoutException, message='Function call timed out'):
#         # print('Hello from __init__')
#         self.time_limit = time_limit
#         print('time_limit = {}'.format(time_limit))
#         self.exception = exception(message)
        
#     def __call__(self, function):
#         # print('Hello from __call__ before wrapped()')
#         def wrapped(*args, **kwargs):
#             # print('Hello from wrapped() inside __call__')
#             signal.signal(signal.SIGALRM, self._raise_exc)
#             signal.alarm(self.time_limit)
#             try:
#                 return function(*args, **kwargs)
#             finally:
#                 signal.alarm(0)
#         return wrapped
        
#     def _raise_exc(self, signum, stack):
#         raise self.exception

def timeout(time_limit, exception=FunctionTimeoutException, message='Function call timed out'):
    """Decorator that raises an exception is the decorated function's execution
    time exceeds the amount of time specified in the decorator."""
    
    def outside_wrapper(function):
        """Outside wrapper function."""
        
        def raise_exception(signum, stack):
            """Raises the exception specified in the timout decorator."""
            raise exception(message)
        
        @functools.wraps(function)
        def inside_wrapper(*args, **kwargs):
            """Inside wrapper function. Uses signal to set up an alarm that goes 
            off if the decorated function's execution time is too high."""
            signal.signal(signal.SIGALRM, raise_exception)
            signal.alarm(time_limit)
            try:
                result =  function(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result
    
        return inside_wrapper
            
    return outside_wrapper

# @timeout(2)
# def my_func(num):
#     """Function used to test the timeout decorator."""
#     time.sleep(num)
#     print('In my_func(): num = {}'.format(num))
#     return num

# help(my_func)
# number = my_func(2)
# print('number = {}'.format(number))


################################################################################
# class timeout(object):
#     def __init__(self, func):
#         self.func = func
#         print('self.func = {}'.format(self.func))
    
#     def __call__(self, function):
#         def wrapped(*args, **kwargs):
#             print('executing wrapped')
#             print('function = {}'.format(function.__name__))
#             result = function(*args, **kwargs)
#             return result
#         return wrapped
        
# @timeout(2)
# def my_func(num):
#     time.sleep(num)
#     print('In my_func(): num = {}'.format(num))
#     return num
    
# number = my_func(2)
# print('number = {}'.format(number))
################################################################################
        
class count_calls(object):
    """Decorator class that uses a dictionary to keep track of the number of 
    times a function has been called. The keys are the name of a function, and 
    the values are the number of times the function has been called."""
    functions = {}
    
    def __init__(self, function):
        self.function = function
        self.function_name = function.__name__
        count_calls.functions[self.function_name] = 0
        
        # Note: When using class decorators, calling help() on the decorated
        # function will still bring up information on the decorated class.
        # However, the decorated function's __name__ and __doc__ attributes
        # will be updated.
        # https://stackoverflow.com/questions/25973376/functools-update-wrapper-doesnt-work-properly/25973438#25973438
        functools.update_wrapper(self, function)
    
    def __call__(self, *args, **kwargs):
        count_calls.functions[self.function_name] += 1
        return self.function(*args, **kwargs)
    
    def counter(self):
        """Returns the number of times the decorated function has been called."""
        return count_calls.functions[self.function_name]
    
    @classmethod
    def counters(cls):
        """Class method that returns the number of times each function has been 
        called."""
        return cls.functions

    @classmethod
    def reset_counters(cls):
        """Class method that resets the functions dictionary."""
        cls.functions = {}

# @count_calls
# def my_func():
#     """Tests count_calls decorator."""
#     pass
# my_func()
# my_func()
# my_func()
# my_func()

# @count_calls
# def other_func():
#     """Tests count_calls decorator."""
#     pass

# help(my_func)
# other_func()

# print('my_func.counter() = {}'.format(my_func.counter()))
# print('other_func.counter() = {}'.format(other_func.counter()))
# print('count_calls.counters() = {}'.format(count_calls.counters()))
# count_calls.reset_counters()
# print('executing count_calls.reset_counters()')
# print('count_calls.counters() = {}'.format(count_calls.counters()))


def inspect(op):
    def wrapped(a, b, operation='add'):
        if operation == 'add':
            result = op(a, b)
            print('{} invoked with {}, {}. Result: {}'.format(op.__name__, a, b, result))
        else:
            result = op(a, b, operation)
            print('{} invoked with {}, {}, operation={}. Result: {}'.format(op.__name__, a, b, operation, result))
        return result
    return wrapped
    
# @inspect
# def calculate(a, b, operation='add'):
#     if operation == 'add':
#         return a + b
#     if operation == 'subtract':
#         return a - b
        
# calculate(5, 4)

class memoized(object):
    
    def __init__(self, function):
        self.function = function
        self.function_name = function.__name__
        self.cache = {}
        print('function name =', self.function_name)
    
    def __call__(self, *args, **kwargs):
        sorted_args = tuple(sorted(args))
        sorted_kwargs = tuple(sorted(kwargs))
        all_args = (sorted_args, sorted_kwargs)

        if sorted_args not in self.cache.keys():
            result = self.function(*args, **kwargs)
            self.cache[sorted_args] = result
            return result
            
        return self.cache[sorted_args]

# @memoized
# def func1(num):
#     pass
# print('executing func1')
# func1(1)
# print()

# @memoized
# def func2(num1, num2):
#     pass
# print('executing func2')
# func2(2, 1)
# print()

# print('executing func1 again')
# func1(1)



