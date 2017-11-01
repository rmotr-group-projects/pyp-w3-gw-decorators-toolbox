# implement your decorators here.
import time
import datetime
import logging 
import signal
from collections import defaultdict
from functools import wraps
import csv
from decorators_library.exceptions import FunctionTimeoutException


def inspect(fn):
    @wraps(fn)
    def dec(*args, **kwargs):
        result = fn(*args, **kwargs)
        args_str = ", ".join(map(str, args))
        kwargs_str = ", ".join(["{}={}".format(k, v) for k, v in kwargs.items()])
        print ("{} invoked with {}. Result: {}".format(fn.__name__, ", ".join(filter(None,[args_str, kwargs_str])), str(result)))
        return result
    return dec

class count_calls(object):
    call_dict = defaultdict(int)
    def __init__(self, fn):
        self.fn = fn
    
    def __call__(self, *args, **kwargs):
        count_calls.call_dict[self.fn.__name__]+=1
        return self.fn(*args, **kwargs)

    def counter(self):
        return count_calls.call_dict[self.fn.__name__]

    @classmethod
    def counters(cls):
        return cls.call_dict

    @classmethod
    def reset_counters(cls):
        cls.call_dict = defaultdict(int)
            

# Executing "my_add" with params: (1, 2), {}
# Finished "my_add" execution with result: 3
class debug(object):
    def __init__(self, logger=None):
        if logger is not None:
            self.logger = logger
        else:
            self.logger = logging.getLogger("tests.test_decorators")
    def __call__(self, fn): 
        @wraps(fn)
        def wrapper(*args, **kwargs):
            self.logger.debug("Executing \"{}\" with params: {}, {}".format(fn.__name__, args, kwargs))
            ret = fn(*args, **kwargs)
            self.logger.debug("Finished \"{}\" execution with result: {}".format(fn.__name__, ret))
            return ret
        return wrapper
    


class timeout(object):
    def __init__(self, timeout_seconds, exception=FunctionTimeoutException):
        self.timeout_seconds=timeout_seconds
        self.exception = exception
        signal.signal(signal.SIGALRM, self.receive_alarm)

    def __call__(self, fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            signal.alarm(self.timeout_seconds)
            ret = fn(*args, **kwargs)
            signal.alarm(0)
            return ret
        return wrapper
        
    def receive_alarm(self, signum, stack):
        raise self.exception('Function call timed out')


        
class memoized(object):
    def __init__(self, fn):
        self.fn = fn
        self.cache = {}
    def __call__(self, *args, **kwargs):
        # if (args, tuple(kwargs.items())) in self.cache:
        #     return self.cache[(args, tuple(kwargs.items()))]
        # ret = self.fn(*args, **kwargs)
        # self.cache[(args, tuple(kwargs.items()))] = ret
        if args in self.cache:
            return self.cache[args]
        ret = self.fn(*args)
        self.cache[args] = ret
        
            
        return ret
    


def func_timer(fn):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        ret = fn(*args, **kwargs)
        end_time = time.time()
        print ("Elapsed time: {:8.7f} seconds".format(end_time-start_time))
        return ret
    return wrapper
    

class auditor(object):
    def __init__(self, file_output="auditor.csv"):
        self.file_output = file_output
    def __call__(self, fn):
        def wrapper(*args, **kwargs):
            invocation_time = str(datetime.datetime.now())
            function_name = fn.__name__
            function_args = args
            function_kwargs = kwargs
            function_result = fn(*args, **kwargs)
            with open(self.file_output, 'a') as csvfile:
                filewriter = csv.writer(csvfile)
                filewriter.writerow([invocation_time, function_name, function_args, kwargs, function_result])
            return function_result
        return wrapper



