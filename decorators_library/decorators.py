# implement your decorators here.
import time 
import signal
import logging
from . import exceptions

"""
@debug()
logging.getLogger(f.__module__)
@debug('my cool logger')
logging.getLogger('my cool logger')
"""

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
        

"""        
my_logger = logging.getLogger(f.__module__)
my_logger.error('Cool log entry bro.')
('decorators_libary.decorators', 'ERROR', 'Cool log entry bro.')
"""

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
"""
def my_dec(f): # Block 1
    def wrap(*args): # Block 2
        return f(*args)
    return wrap'''
    
class my_dec(object):
    def __init__(self, f): # Block 1
        self.f = f
    def __call__(self, *args): # Block 2
        return self.f(*args)
        
def my_dec_with_param(param): # Block 1
    def deco(f): # Block 2
        def wrap(*args): # Block 3
            return f(*args)
        return wrap
    return deco
    
class my_dec_with_param(object):
    def __init__(self, param): # Block 1
        self.param = param
    def __call__(self, f): # Block 2
        def wrap(*args): # Block 3
            return f(*args)
        return wrap

my_func = my_dec(f) wrap(f)(args) # function
my_func = my_dec(f) my_dec_instance(args) # class
"""


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
                
"""                
signal.signal(signal_to_wait_for, function_to_call_when_signal_raised)
signal.alarm(timeout) # Sends signal.SIGALRM after timeout seconds
signal.alarm(0) # clears alarm
"""
"""
@count_calls
def my_func(x, y):
    pass

@count_calls
def my_other_func(x, y):
    pass

my_func()
my_other_func()

count_calls.counts()
{'my_func': 1, 'my_other_func': 1}
"""

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
    
    
    
"""
@count_calls
def my_func(*args):
    return sum(args)

count_calls.counters() >> {'my_func': 0}
{}

my_func = count_calls(my_func) >> count_calls_instance with self.func == my_func

my_func(1,2,3) >> 6
my_func.counter() >> 1


        
class my_class(object):
    my_var = 'Stuff'
    def __init__():
        self.class_variable
    
    def my_meth(self):
        return self
    
    @classmethod
    @property
    def my_prop(self):
        
        return 'Im a property'
        
    @classmethod
    def my_cls(cls):
        return cls.my_var
        
    @staticmethod
    def my_stat():
        return 'Hi'
    
class Person(object):
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        
    @property
    def full_name(self):
        return self.first_name + " " + self.last_name
"""


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