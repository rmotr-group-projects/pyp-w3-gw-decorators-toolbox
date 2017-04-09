# implement your decorators here.

import signal
import logging
import functools
import collections
import time 
import json

from exceptions import TimeoutError, PermissionError

def timeout(seconds, error_message = 'Function call timed out'):
    def decorate_it(funct):
        def when_timed_out(signum, frame):
            raise TimeoutError(error_message)
            
        @functools.wraps(funct)    
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, when_timed_out)
            signal.alarm(seconds)
            
            try:
                output = funct(*args, **kwargs)
            finally:
                signal.alarm(0)
            return output
        return wrapper
    return decorate_it
    
    
class debug(object):
    BEFORE_MSG = 'Executing "{}" with params: {}, {}'
    AFTER_MSG = 'Finished "{}" execution with result: {}'
    
    def __init__(self, logger = None):
        self.logger = logger
    
    def __call__(self, funct):
        if self.logger is None:
            logging.basicConfig()
            self.logger = logging.getLogger(funct.__module__)
            
        @functools.wraps(funct)
        def wrapper(*args, **kwargs):
            self.logger.debug(
                self.BEFORE_MSG.format(funct.__name__, args, kwargs)
            )
            output = funct(*args, **kwargs)
            self.logger.debug (
                self.AFTER_MSG.format(funct.__name__, output)
            )
            return output
        return wrapper
    

class count_calls(object):
    FUNCTION_LIST = {}
    
    def __init__(self, funct):
        self.funct = funct
        self.num  = 0
        count_calls.FUNCTION_LIST[self.funct] = self.num
        
    def __call__(self, *args, **kwargs):
        count_calls.FUNCTION_LIST[self.funct] += 1
        return self.funct(*args, **kwargs)
        
    def counter(self):
        return count_calls.FUNCTION_LIST[self.funct]
        
    @classmethod
    def counters(classes):
        return dict([ (functs.__name__, classes.FUNCTION_LIST[functs]) for functs in classes.FUNCTION_LIST])
        
    @classmethod
    def reset_counters(self):
        count_calls.FUNCTION_LIST = {}
        
    
class memoized(object):
    
    def __init__(self, funct):
        self.funct = funct
        self.cache = {}
        
    def __call__(self, *args):
        # If we can't put args into cache because they are not correct types
        # of arguments 
        if not isinstance(args, collections.Hashable):
            # Just return the funct call
            return self.funct(*args)
        
        if args in self.cache:
            # We did this before so just return the cache
            return self.cache[args]
        else:
            # We'v never don this funct before so lets run and save args and value
            output = self.funct(*args)
            self.cache[args] = output
            return output
            
        
# outputs the time took to execute last function call of that type
class time_me(object):
    
    def __init__(self, funct):
        self.funct = funct
        self.timed = 0.0

    def __call__(self, *args, **kwargs):
        time_start = time.time()
        output = self.funct(*args, **kwargs)
        time_end = time.time()
        
        self.timed = time_end - time_start
        
        return output
        
    @classmethod
    def timed(self):
        return self.time
        
        
# Checks permissions on user
def check_permission(permission, error_message = 'Sorry, you do not have permission for this'):
    
    def decorate_it(funct):
        @functools.wraps(funct)
        def wrapper(user):
            if permission in user.get("permissions"):
                return funct(user)
            else:
                raise PermissionError(error_message)
        return wrapper
    return decorate_it
    

                
        
    
        


        
        
            
        
            
            
        
    
