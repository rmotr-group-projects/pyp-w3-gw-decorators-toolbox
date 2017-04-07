# implement your decorators here.
import time as t
import logging
import threading
from . exceptions import TimeoutError
from datetime import datetime as dt

class timeout(object):
    def __init__(self, timeout):
        self.timeout = timeout
    
    def __call__(self, func):
        def wrapper(*args, **kwargs):
            start = t.time()
            func(*args, **kwargs)
            end = t.time()
            if (end-start) > self.timeout:
                raise TimeoutError
            return func(*args, **kwargs)
        return wrapper
    
class debug(object):
    def __init__(self, logger=None):
        self.logger = logger
        
    def __call__(self, func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if self.logger:
                log = self.logger
                return result
            log = logging.getLogger(func.__module__)
            log.debug('Executing "{}" with params: {}, {}'.format(
                      func.__name__, args, kwargs))
            log.debug('Finished "{}" execution with result: {}'.format(
                      func.__name__, result))
            return result
        return wrapper
   
class memoized(object):
    def __init__(self,func):
        self.func = func
        self.cache = {}
    
    def __call__(self,*args):
        result = self.func(*args)
        if (args[0],args[1]) not in self.cache:
            self.cache[(args[0],args[1])] = result
            return result
        else:
            return self.cache[(args[0],args[1])]

class count_calls(object):
    count = {}
    
    def __init__(self, func):
        self.func = func
        self.count[func.__name__] = 0
        
    def __call__(self, *args):
        self.count[self.func.__name__] += 1
        return self.func(*args)
        
    def counter(self):
        return self.count.get(self.func.__name__)
        
    @classmethod
    def counters(cls):
        return cls.count
        
    @classmethod
    def reset_counters(cls):
        cls.count = {}
        
        
class timelog(object):
    log = {}
    
    def __init__(self, func):
        self.func = func
        
    def __call__(self, *args, **kwargs):
        if self.func.__name__ not in self.log:
            self.log.update({self.func.__name__ : []})
        self.log[self.func.__name__].append("{} called at {}".format(
            self.func.__name__, dt.now().strftime('%Y-%m-%d %H:%M:%S')))
        return self.func(*args, **kwargs)
        
    def get_one_log(self):
        return self.log.get(self.func.__name__)
        
    @classmethod
    def get_log(cls):
        return cls.log
        
    @classmethod
    def clear_log(cls):
        cls.log = {}
        
class opposite(object):
    def __init__(self, func):
        self.func = func
    
    def __call__(self, *args):
        new_args = []
        for arg in args:
            new_args.insert(0,arg)
        return self.func(*new_args)
        

class validarg(object):
    def __init__(self, *types):
        self.types = types
        
    def __call__(self, func, *args):
        def wrapper(*args):
            if len(self.types) != len(args):
                raise IndexError(
                    "Invalid, requires {} arguments, was given {}: {}".format(
                    len(self.types), len(args), args))
            for (x, y) in zip(args, self.types):
                if not isinstance(x, y): 
                    raise TypeError(
                        "Invalid, argument '{}' is not of {}".format(x, y))
            return func(*args)
        return wrapper
        
class sync(object):
    def __init__(self, func):
        self.func = func
        self.lock = threading.Lock()
        
    def __call__(self, *args, **kwargs):
        self.lock.acquire()
        try:
            return self.func(*args, **kwargs)
        finally:
            self.lock.release()
        return self.func(*args, **kwargs)