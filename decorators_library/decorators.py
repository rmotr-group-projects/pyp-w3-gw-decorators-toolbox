import time
import inspect
from .exceptions import TimeoutError
from logging import getLogger
import signal

class Timeout(object):
    def __init__(self, func, max_time):
        self.func = func
        self.max_time = max_time
    
    def __call__(self, *args, **kwargs):
        def handler(signum, frame):
            raise TimeoutError('Function call timed out')
        
        # Set the signal handler and a 5-second alarm
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(self.max_time)
        return_val = self.func(*args, **kwargs)
        signal.alarm(0)  
        
        return return_val

def timeout(max_time):
    def decorator(func):
        return Timeout(func, max_time)
    return decorator
    
def debug(logger=None):
    def other(func):
        def wrapper(*args, **kwargs):
            return_val = func(*args, **kwargs)
            if logger is not None:
                log = logger
            else:  
                log = getLogger('tests.test_decorators')
                
            log.debug('Executing "{}" with params: {}, {{}}'.format(func.__name__, tuple(args)))
            log.debug('Finished "{}" execution with result: {}'.format(func.__name__, return_val))
                
            return return_val
        return wrapper
    return other
  
class count_calls(object):
    
    func_calls = {}
    
    def __init__(self,func):
        self.func = func
        self.func_name = func.__name__
        self.func_calls.setdefault(self.func_name, 0)
        

    def counter(self):
        return self.func_calls[self.func_name]
        
    @classmethod
    def counters(self):
        return self.func_calls
        
    @classmethod
    def reset_counters(self):
        self.func_calls = {}
    
    def __call__(self, *args, **kwargs):
        self.func_calls[self.func_name] += 1
        
        return self.func(*args, **kwargs)
    
class memoized:
    def __init__(self, func):
        self.func = func
        self.cache = {}
        
    def __call__(self, *args, **kwargs):
        if tuple(args) in self.cache:
            return self.cache[args]
            
        return_val = self.func(*args, **kwargs)
        self.cache[args] = return_val
        return return_val
        
    
def assert_type(*args, **kwargs):
    """Decorator that does type checking for each parameter."""
    type_list = list(args)
    type_dict = kwargs
    
    def decorator(func):
        def wrapper(*args, **kwargs):
            
            if len(type_list) + len(type_dict) != len(args) + len(kwargs):
                expected = len(inspect.getargspec(func).args)
                received = len(args) + len(kwargs)
                raise ValueError("Wrong number of arguments. Expected: {}; Received: {}".format(expected, received))
                
            type_args = [type(val) for val in args]
            type_kwargs = [kwargs[key] for key in type_dict] 
            
            if type_args != type_list or not all([type_dict[key] == kwargs[key] for key in type_dict]):
                expected = tuple(type_list + [type_dict[key] for key in type_dict])
                received = tuple(type_args + type_kwargs)
                error_msg = "Wrong type. Expected: {}; Received: {}".format(get_type(expected), get_type(received))
                
                raise TypeError(error_msg) 
                
            return func(*args, **kwargs)
        return wrapper
    return decorator

def get_type(type_list):
    return tuple(type_.__name__ for type_ in type_list) 

class running_time:
    """measures the running time each time the function is called and stores it in a list"""
    def __init__(self, func):
        self.func = func
        self.running_times = []
        
    def __call__(self, *args, **kwargs):
        start = time.time()
        return_val = self.func(*args, **kwargs)
        end = time.time()
        self.running_times.append(end - start)
        return return_val
    
    def average_time(self):
        return sum(self.running_times) / len(self.running_times)
        
    def counter(self):
        return len(self.running_times)
        
    def min_running_time(self):
        return min(self.running_times)
        
    def max_running_time(self):
        return max(self.running_times)