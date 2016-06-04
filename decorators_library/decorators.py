import logging
import signal

from .exceptions import TimeoutError


class debug(object):
    
    def __init__(self, logger=None):
        self.logger = logger

    def __call__(self, func):
        if not self.logger:
            logging.basicConfig()
            log = logging.getLogger(func.__module__)
            log.setLevel(logging.DEBUG)
        else:
            log = self.logger
        
        def func_wrapper(*args, **kwargs):
            startmessage = 'Executing "{}" with params: {}, {}'.format(func.__name__, args, kwargs)
            log.debug(startmessage)
            results = func(*args, **kwargs)
            endmessage = 'Finished "{}" execution with result: {}'.format(func.__name__, results)
            log.debug(endmessage)
            return results
        return func_wrapper

def timeout(time):
    def wrapper(func):
        def handler(signum, frame):
            raise TimeoutError('Function call timed out')        
        
        def run_in_timer():
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(time)
            func()
            signal.alarm(0)
        return run_in_timer
    return wrapper


class count_calls(object):
    # We init this dict outside of __init__ so static methods can access it.
    count_dict = {}
    
    def __init__(self, func):
        self.func = func
        self.count = 0
        # Now we pass in our self object, into the dict, so we can locate them in our static methods.
        count_calls.count_dict[func] = self 

    def __call__(self, *args, **kwargs):
        self.count += 1
        count_calls.count_dict[self.func].count = self.count # store updated result in the class dict
        return self.func(*args, **kwargs)
 
    def counter(self):
        return count_calls.count_dict[self.func].count

    @classmethod
    def counters(cls):
        resultdict = {}
        for func in cls.count_dict:
            resultdict[func.__name__] = cls.count_dict[func].count
        return resultdict
    
    @classmethod
    def reset_counters(cls):
        cls.count_dict = {}
        
        
class memoized(object):
    def __init__(self, func):
        self.func = func
        self.cache = {}
      
    def __call__(self, *args):
        if args in self.cache:
            return self.cache[args]
        else:
            value = self.func(*args)
            self.cache[args] = value
            return value

# our two original new decorators

def plocker(func):
    ''' Process locker, so the function only runs a single thread at a time.
    Example:
    
    '''
    pass

def insecure_function(func):
    '''
    This decorator will warn people there are security concerns with the decorated function
    by raising a SecurityError that they'll need to swallow to use the function.
    Perhaps by adding INSECURE=yes as a parameter?  This decorator then strips that off
    and runs the function anyway.
    '''
    
