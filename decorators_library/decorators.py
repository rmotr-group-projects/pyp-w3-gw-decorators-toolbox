import logging
import time
import signal
from .exceptions import TimeoutError

def debug(logger=None):
    def debug_decorator(f):
        def wrapped(*args, **kwargs):
            # handle setting the getLogger(*name*)
            if logger is None:
                the_logger = logging.getLogger(f.__module__)
            else:
                the_logger = logger
            # do the actual work expected from the decorator
            the_logger.debug('Executing "{}" with params: {}, {}'.format(f.__name__, args, kwargs))
            result = f(*args, **kwargs)
            the_logger.debug('Finished "{}" execution with result: {}'.format(f.__name__, result))
            return result
        return wrapped
    return debug_decorator

    
class count_calls(object):
    count_dict = {}
    
    def __init__(self, f):
        self.f = f
        count_calls.count_dict[f.__name__] = 0
        
    def __call__(self, *args, **kwargs):
        count_calls.count_dict[self.f.__name__] += 1
        return self.f(*args, **kwargs)
    
    def counter(self):
        return count_calls.count_dict[self.f.__name__]
        
    @classmethod
    def counters(cls):
        return cls.count_dict
        
    @classmethod
    def reset_counters(cls):
        cls.count_dict.clear()
        

class memoized(object):
    def __init__(self, f):
        self.f = f
        self.cache = {}
        
    def __call__(self, *args, **kwargs):
        if args in self.cache:
            return self.cache[args]
        value = self.f(*args, **kwargs)
        self.cache[args] = value
        return value
        
        
def timeout(seconds):
    def timeout_decorator(f):
        def _handle_timeout(signum, frame):
            raise TimeoutError('Function call timed out')
 
        def wrapper(*args, **kwargs):
            """
            start the timer using signal
            try to run the function
            
            """
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                return f(*args, **kwargs)
            finally:
                # cancels the alarm if successful
                signal.alarm(0)
        return wrapper
    return timeout_decorator
    

def timer(f):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        value = f(*args, **kwargs)
        end_time = time.time()
        the_logger = logging.getLogger(f.__module__)
        the_logger.debug("It took {} {:.2f} seconds to run.".format(f.__name__, end_time - start_time))
        return value
    return wrapper

# clip function

def retry(limit):
    def retry_decorated(f):
        count = 0
        def wrapper(*args, **kwargs):
            nonlocal count
            if count < limit:
                try:
                    return f(*args, **kwargs)
                except:
                    count += 1
                    return wrapper(*args, **kwargs)
            raise TimeoutError("Too many tries")
                
        return wrapper
    return retry_decorated
    

def clipper(limit):
    def clipper_decorated(f):
        def wrapper(*args, **kwargs):
            original_result = f(*args, **kwargs)
            if limit <= original_result:
                return limit
            return original_result
        return wrapper
    return clipper_decorated
                


"""    
@timer
def foo():
    time.sleep(1)
    print("hello")
    
foo()
"""

"""
num_tries = 0

@retry(2)
def dumb_fail():
    global num_tries
    if num_tries == 3:
        print("Success!")
    else:
        num_tries += 1
        raise TypeError
    
dumb_fail()
"""