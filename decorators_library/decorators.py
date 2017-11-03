# implement your decorators here.
from decorators_library.exceptions import *
import time
import signal

def inspect(function):
    def wrapper(*args, **kwargs):
        kwargList = tuple('{}={}'.format(key, val) for key, val in kwargs.items())
        arg_str = ', '.join(map(str, args + kwargList))
        fn = function(*args, **kwargs)
        print('{} invoked with {}. Result: {}'.format(function.__name__, arg_str, str(fn)))
        return fn
    return wrapper

def timeout(val, exception = FunctionTimeoutException):
    def timeout_fn(function):
        def wrapper(*args, **kwargs):
            def receive_alarm(signum, stack):
                raise exception("Function call timed out")
            signal.signal(signal.SIGALRM, receive_alarm)
            signal.alarm(val)
            fn = function(*args, **kwargs)
            return fn
        return wrapper
    return timeout_fn
        
    
def debug(function):
    def wrapper(*args, **kwargs):
        print('Executing {} with params: {}, {}').format(function.__name__, args, kwargs)
        fn = function(*args, **kwargs)
        print('Finished {} execution with result: {}').format(function.__name__, str(fn))
        return fn
    return wrapper

class count_calls(object):
    countDict = {}
    
    def __init__(self, function):
        self.function = function
        iter(self)
        
    def __iter__(self):
        self.countVal = 0
        return self
        
    def __next__(self):
        count = self.countVal
        self.countVal += 1
        return count
    
    def counter(self):
        count_calls.countDict[self.function.__name__] = self.countVal
        return self.countVal
        
    @classmethod
    def counters(cls):
        return cls.countDict
        
    @classmethod
    def reset_counters(cls):
        return cls.countDict.clear()
        
    def __call__(self, *args, **kwargs):
        next(self)
        return self.function(*args, **kwargs)
        

class memoized(object):
    def __init__(self, function):
        self.function = function
        self.cache = {}
    
    def __call__(self, *args, **kwargs):
        kwargList =  tuple('{}={}'.format(key, val) for key, val in kwargs.items())
        allArgs = args + kwargList
        if allArgs in self.cache:
            return self.cache[allArgs]
        else:
            fn = self.function(*args, **kwargs)
            self.cache[allArgs] = fn
            return fn

# check if args is str or num
def contract(arg):
    def contract_fn(function):
        def wrapper(*args, **kwargs):
            kwarg_vals = tuple(kwargs.values())
            lst = args + kwarg_vals
            if arg == "numeric":
                if all(isinstance(x, (int, float)) for x in lst):
                    return function(*args, **kwargs)
                else:
                    raise NotNumericException
            elif arg == "string":
                if all(isinstance(x, str) for x in lst):
                    return function(*args, **kwargs)
                else:
                    raise NotStringException
        return wrapper
    return contract_fn
    
#  logs run time
def logRunTime(function):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        fn = function(*args, **kwargs)
        duration = time.time - start_time
        return fn
    return wrapper

