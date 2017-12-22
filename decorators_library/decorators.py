from decorators_library.exceptions import FunctionTimeoutException
import functools
import time
import sys
import signal
import logging

def timeout(time_limit, exception=FunctionTimeoutException, message='Function call timed out'):
    """
    Decorator that raises an exception is the decorated function's execution
    time exceeds the amount of time specified in the decorator.
    """
    
    def outside_wrapper(function):
        """Outside wrapper function."""
        
        def raise_exception(signum, stack):
            """Raises the exception specified in the timout decorator."""
            raise exception(message)
        
        @functools.wraps(function)
        def inside_wrapper(*args, **kwargs):
            """
            Inside wrapper function. Uses signal to set up an alarm that goes 
            off if the decorated function's execution time is too high.
            """
            signal.signal(signal.SIGALRM, raise_exception)
            signal.alarm(time_limit)
            try:
                result =  function(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result
    
        return inside_wrapper
            
    return outside_wrapper

        
class count_calls(object):
    """
    Decorator class that uses a dictionary to keep track of the number of 
    times a function has been called. The keys are the name of a function, and 
    the values are the number of times the function has been called.
    """
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


def inspect(op):
    """
    This decorator is prints the decorated function's name, parameters, and 
    calculated value to the screen.
    """
    
    @functools.wraps(op)
    def wrapped(a, b, operation='add'):
        if operation == 'add':
            result = op(a, b)
            print('{} invoked with {}, {}. Result: {}'.format(op.__name__, a, b, result))
        else:
            result = op(a, b, operation)
            print('{} invoked with {}, {}, operation={}. Result: {}'.format(op.__name__, a, b, operation, result))
        return result
        
    return wrapped
    

class memoized(object):
    """
    This decorator keeps track of previous executions of the decorated 
    function and the result of the invokations. If the decorated function is 
    executed again using the same set of arguments sent in the past, the result 
    must be immediately returned by an internal cache instead of re-executing 
    the same code again.
    """
    def __init__(self, function):
        self.function = function
        self.function_name = function.__name__
        self.cache = {}
        
        # Note: When using class decorators, calling help() on the decorated
        # function will still bring up information on the decorated class.
        # However, the decorated function's __name__ and __doc__ attributes
        # will be updated.
        # https://stackoverflow.com/questions/25973376/functools-update-wrapper-doesnt-work-properly/25973438#25973438
        functools.update_wrapper(self, function)
    
    def __call__(self, *args, **kwargs):
        sorted_args = tuple(sorted(args))
        sorted_kwargs = tuple(sorted(kwargs))
        all_args = (sorted_args, sorted_kwargs)

        if sorted_args not in self.cache.keys():
            result = self.function(*args, **kwargs)
            self.cache[sorted_args] = result
            return result
            
        return self.cache[sorted_args]


class debug(object):
    """
    This decorator debugs the executions of the decorated function by 
    logging a message before starting the execution (function name, args, 
    kwargs), and a second message after the execution is finished with the 
    returned result (function name, returned value).
    """
    def __init__(self, logger=None):
        self.logger = logger
    
    def __call__(self, function, *args, **kwargs):
        if not self.logger:
            logging.basicConfig()
            self.logger = logging.getLogger(function.__module__)
            self.logger.setLevel(logging.DEBUG)
        
        @functools.wraps(function)
        def wrapped(*args, **kwargs):
            self.logger.debug('Executing "{}" with params: {}, {}'.format(function.__name__, args, kwargs))
            result = function(*args, **kwargs)
            self.logger.debug('Finished "{}" execution with result: {}'.format(function.__name__, result))
            return result
        return wrapped