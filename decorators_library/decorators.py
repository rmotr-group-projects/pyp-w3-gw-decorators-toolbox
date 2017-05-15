# implement your decorators here.
import time 
import signal
import logging
from .exceptions import *


class debug(object):
    def __init__(self, logger=None):
        self.logger = logger
        
    def __call__(self, func):
        if self.logger is None:
            self.logger = logging.getLogger(func.__module__)
        
            
        def wraps(*args, **kwargs):
            self.logger.debug('Executing "{}" with params: {}, {}'.format(func.__name__, args, kwargs))
            res = func(*args, **kwargs)
            self.logger.debug('Finished "{}" execution with result: {}'.format(func.__name__, res))
            return res
        return wraps
        

class memoized(object):
    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        
        if args in self.cache.keys():
            return self.cache[args]
        else:
            self.cache[args] = self.func(*args)
            return self.cache[args]


def timeout(sMax):
    def real_dec(function):
        def wrapper(*args):
            def handler(sigTrigger, res):
                raise TimeoutError("Function call timed out")
                
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(sMax)
            
            results = function(*args)
            
            signal.alarm(0)
            return results

        return wrapper
    return real_dec    
                

class count_calls(object):


    counters_dict = {}
    
    def __init__(self, func):
        self.func = func
        count_calls.counters_dict[func.__name__] = 0

    def __call__(self, *args):
        result = self.func(*args)    
        count_calls.counters_dict[self.func.__name__] += 1
        return result

    @classmethod
    def reset_counters(cls):
        cls.counters_dict = {}
    
    @classmethod    
    def counters(cls):
        return cls.counters_dict
        
    def counter(self):
    
        count = count_calls.counters_dict[self.func.__name__]
        return count
        
'''
Decorator function 'func_stopwatch' calculates and logs the total runtime of any decorated function.
func_stopwatch has a reset function that destroys the log file.

    returns the result of executing 'orig_func'
    
    logs:
       -tested function's name
       -list of params passed to function
       -list of dicts passed to function
       -total runtime
       -return value of 'orig_func'
'''
class func_stopwatch(object):
    count = 0
    
    def __init__(self, orig_func):
        self.orig_func = orig_func
    
    def __call__(self,*args, **kw):
        def wrapper():
            t1 = time.time()
            res = self.orig_func(*args, **kw)
            runtime = time.time() - t1
            try:
                with open('log.txt', 'a') as logf:
                    logf.write("ENTRY #{}\nStart time: {}\nCompleted execution of function {} with params: {}, {}\nTotal runtime:{}\nreturned:\n   Type: {}\n   Value: {}\n\n".format(func_stopwatch.count, t1, self.orig_func.__name__, args, kw, runtime, type(res), res))
                    logf.close()
            except:
                 with open('log.txt', 'w+') as logf:
                    logf.write("[Began: {}]\nEnding function {} with params: {}, {}\nTotal runtime:{}\nreturned:\n   Type: {}\n   Value: {}\n\n".format(t1, self.orig_func.__name__, args, kw, runtime, type(res), res))
                    logf.close()
            return res
            
        func_stopwatch.count += 1
        return wrapper
    
    @classmethod
    def reset(cls):
        cls.count = 0
        try:
            from os import remove as rm; rm('log.txt')
            print('log.txt deleted.')
        except:
            print('No log file found to delete.')


def retry(max_attempts, delay = 1, delay_factor = 2, exceptions = (Exception,)):

    """ max_attempts = how many times to retry function
    delay = sleep time in seconds between attempts
    delay_factor = increase delay by this multiple in between attempts
    !! USE A SENSIBLE delay_factor !! otherwise you could have an exponential wait
    exceptions = tuple of exceptions that will trigger the retry, defaults to any Exception """

    def retry_dec(func):
        def wrapper(*args, **kwargs):
            wrapper_delay = delay
            attempts = range(max_attempts)
            attempts.reverse()
            for attempts_left in attempts:
                try:
                   return func(*args, **kwargs)
                except exceptions:
                    if attempts_left > 0:
                        time.sleep(wrapper_delay)
                        wrapper_delay = wrapper_delay * delay_factor
                    else:
                        raise 
                else:
                    break
        return wrapper
    return retry_dec