# implement your decorators here.
from time import sleep
import time
import signal
import logging

from decorators_library.exceptions import *


def timeout(max_time):
    def decorate(func):
        def handler(signum, frame):
            # print("Here")
            raise TimeoutError()
            
        def new_f(*args, **kwargs):
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(max_time)
            
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result
        new_f.func_name = func.func_name
        return new_f
    return decorate


class count_calls(object):
    collections_counter = {}
    
    def __init__(self, f):
        self.f = f
        self.__class__.collections_counter[f.__name__] = 0
        
    def __call__(self, *args, **kwargs):
        
        if self.f.__name__ in self.__class__.collections_counter:
            self.__class__.collections_counter[self.f.__name__] += 1
        else:
            self.__class__.collections_counter[self.f.__name__] = 1
        
    def counter(self):
        print("Printing self.counter(): {}".format(self.collections_counter))
        print("Printing type: {}".format(type(self.collections_counter)))
        return self.__class__.collections_counter[self.f.__name__]

        
    @classmethod
    def counters(cls):
        print("Printing cls.collections_counter: {}".format(cls.collections_counter))
        print("Printing type: {}".format(type(cls.collections_counter)))
        return cls.collections_counter
        
    @classmethod
    def reset_counters(cls):
        cls.collections_counter = {}
        

class debug():
    def __init__(self, logger=None):
        self.logger = logger
        
    def __call__(self, f):
        f_name = f.__name__
        
        def wrapper(*args, **kwargs):
            if self.logger is None:
                logging.basicConfig()
                self.logger = logging.getLogger(f.__module__)
            
            before = "Executing {}{}{} with params: {}, {}".format('"', f_name,'"', args, kwargs)
            result = f(*args, **kwargs)
            after = "Finished {}{}{} execution with result: {}".format('"', f_name,'"',result)

            self.logger.debug(before)
            self.logger.debug(after)
                      
            return result
        return wrapper


class memoized(object):
    def __init__(self, f):
        self.cache = {}
        self.f = f
    
    def __call__(self, *args):
        #print('cache =',self.cache)
        key = args
        if key in self.cache:
            return self.cache[key]
        else:
            result = self.f(*args)
            self.cache[key] = result
            return result