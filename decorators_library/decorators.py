import signal
import .exceptions
import logging
import time

def timeout_occured(signum, frame):
    if timeout.running:
        raise exceptions.TimeoutError('Function call timed out')
    
def timeout(time):
    def timeout_decorator(func):
        def run_timeout(*args, **kwargs):
            signal.signal(signal.SIGALRM, timeout_occured)
            signal.alarm(time)
            timeout.running = True
            result = func(*args, **kwargs)
            timeout.running = False
            return result
        return run_timeout
    return timeout_decorator
            
def debug(logger=None):
    def logging_decorator(func):
        def log_function(*args, **kwargs):
            if not logger:
                debug_logger = logging.getLogger(func.__module__)
            else:
                debug_logger = logger
            debug_logger.debug('Executing "{}" with params: {}, {}'.format(func.__name__, args, kwargs))
            result = func(*args, **kwargs)
            debug_logger.debug('Finished "{}" execution with result: {}'.format(func.__name__, result))
            return result
        return log_function
    return logging_decorator

class count_calls():
    counters_dict = {}
    
    def __init__(self, func):
        self.func = func
        self.counters_dict[func.__name__] = 0
        
    def __call__(self, *args, **kwargs):
        new_count = self.counters_dict.get(self.func.__name__, 0) +1
        self.counters_dict[self.func.__name__] = new_count
        return self.func(*args, **kwargs)
        
    @classmethod
    def counters(cls):
        return cls.counters_dict
        
    @classmethod
    def reset_counters(cls):
        cls.counters_dict = {}
        
    def counter(self):
        return self.counters_dict.get(self.func.__name__, 0)
        
def memoized(func):
    def memo_function(*args, **kwargs):
        if not hasattr(memo_function, "cache"):
            setattr(memo_function, "cache", {})
        result = func(*args, **kwargs)
        memo_function.cache[args] = result
        return func(*args, **kwargs)
    return memo_function
    
def stopwatch(func):

# Times how long a function takes to run and stores it in
# function.elapsed_time

    def time_function(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        setattr(time_function, 'elapsed_time', time.time() - start_time)
        return func(*args, **kwargs)
        
    return time_function
        

def reverse(func):
    '''Assumes func returns a string or list or tuple'''
    def reverse_function(*args, **kwargs):
        reverse = func(*args, **kwargs)[::-1]
        return reverse
        
    return reverse_function
        