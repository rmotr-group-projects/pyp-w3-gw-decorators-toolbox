from functools import wraps
from decorators_library.exceptions import FunctionTimeoutException
import signal
import logging


def inspect(fn):
    @wraps(fn)
    def new_fn(*args, **kwargs):
        # Convert kwargs into tuple in format: key=value, so can be added to args
        kwarg_lst = tuple('{}={}'.format(key, val) for key, val in kwargs.items())
        # Convert args & kwargs to string for printing
        arg_str = ', '.join(map(str,args  + kwarg_lst))
        fn_result = fn(*args, **kwargs)
        
        print('{} invoked with {}. Result: {}'.format(fn.__name__, arg_str, str(fn_result)))
        return fn_result
    return new_fn

class timeout(object):
    def __init__(self, duration, exception=FunctionTimeoutException):
        self.duration = duration
        self.exception = exception
    
    def raise_alarm(self, signum, stack):
        raise self.exception("Function call timed out")

    def __call__(self, fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            # Create alarm to be raised at duration passed
            signal.signal(signal.SIGALRM, self.raise_alarm)
            signal.alarm(self.duration)
            return fn(*args, **kwargs)
        # Turn off alarm if it wasn't set off
        signal.alarm(0)
        return wrapped

class debug(object):
    def __init__(self, logger=logging.getLogger('tests.test_decorators')):
        self.logger = logger
  
    def __call__(self, fn):
        @wraps(fn)
        def new_fn(*args, **kwargs):
            # Convert kwargs & args into strings for logging
            kwarg_lst = ', '.join(['{}={}'.format(key, val) for key, val in kwargs.items()])
            arg_str = ', '.join(map(str,args))
            
            # First log parameters being used
            self.logger.debug('Executing "{}" with params: ({}), {{{}}}'.format(fn.__name__, arg_str, kwarg_lst))
            fn_result = fn(*args, **kwargs)
            # After running function log execution results
            self.logger.debug('Finished "{}" execution with result: {}'.format(fn.__name__, str(fn_result)))
            return fn_result
        return new_fn

class count_calls(object):
    FN_CALLS = {}
  
    def __init__(self, fn):
        self.fn = fn
        # Initialize the dictionary entry for this function
        self.FN_CALLS[self.fn.__name__] = 0
  
    def __call__(self, *args, **kwargs):
        # Increment stored value in the dictionary and return function
        self.FN_CALLS[self.fn.__name__] += 1
        return self.fn(*args, **kwargs)
  
    def counter(self):
        # Get value from dictionary for function currently being used
        return self.FN_CALLS[self.fn.__name__]
  
    @classmethod
    def counters(cls):
        # Return entire dictionary of counters
        return cls.FN_CALLS
  
    @classmethod
    def reset_counters(cls):
        # Reset dictionary to empty dict
        cls.FN_CALLS.clear()
    

def memoized(fn):
    cache = {}
    
    @wraps(fn)
    def new_fn(*args):
        # Check if the function call is already in the cache
        if args in cache:
            # If so return stored function output from cache
            return cache[args]
        else:
            # If not add to the cache
            fn_result = fn(*args)
            cache[args] = fn_result
            return fn_result
    
    new_fn.cache = cache
    return new_fn