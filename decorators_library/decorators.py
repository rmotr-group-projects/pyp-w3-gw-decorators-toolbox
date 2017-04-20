import logging
import time
import re
import functools
from functools import wraps
import datetime as dt
from . import exceptions
import signal


class timeout(object):
    
    def __init__(self, t_out):
        self.t_out = t_out
        
    def __call__(self, func):
        
        def sig_handle(signum, stack):
            raise exceptions.TimeoutError('Function call timed out')
        
        @wraps(func)
        def ret_timeout(*args,**kwargs):
            
            #sig_handle = lambda s, s : raise exceptions.TimeoutError('Function call timed out')
            #The above doesnt work, why?
            signal.signal(signal.SIGALRM, sig_handle )
            signal.alarm(self.t_out)

            results = func(*args,**kwargs)
            return results
            
        return ret_timeout


class debug(object):

    def __init__(self, logger=None):
        self.logger = logger

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not self.logger:
                logging.basicConfig(level='DEBUG')
                self.logger = logging.getLogger(func.__module__)
            self.logger.debug('Executing "%s" with params: %s, %s', func.__name__,
                        args, kwargs)
            result = func(*args, **kwargs)
            self.logger.debug('Finished "%s" execution with result: %s',
                              func.__name__, result)
            return result
        return wrapper
        

class memoized(object):

    def __init__(self, func):
        self.func = func
        self.cache = {}
        functools.update_wrapper(self, func)

    def __call__(self, *args, **kwargs):
        if args in self.cache:
            return self.cache[args]
        result = self.func(*args, **kwargs)
        self.cache[args] = result
        return result
        

class count_calls(object):
    all_dict = {}

    def __init__(self, func):
        self.func = func
        count_calls.all_dict[self.func.__name__] = 0
        functools.update_wrapper(self, func)

    def __call__(self, *args, **kwargs):
        count_calls.all_dict[self.func.__name__] += 1
        return self.func(*args, **kwargs)

    def counter(self):
        return count_calls.all_dict[self.func.__name__]

    @classmethod
    def reset_counters(cls):
        cls.all_dict = {}

    @classmethod
    def counters(cls):
        return cls.all_dict
        

class WordReplace(object):

    def __init__(self, org_word, replacement):
        self.org_word = org_word
        self.replace = replacement

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args):
            new_text = re.sub(self.org_word, self.replace, args[0], flags=re.I)
            new_args = (new_text,) + args[1:]
            return func(*new_args)
        return wrapper


def retry(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        tries = 1
        while True:
            result = func(*args, **kwargs)
            if result == False and tries < 3:
                tries += 1
                continue
            break
        return result
    return wrapper