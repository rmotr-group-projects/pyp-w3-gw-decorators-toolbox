# implement your decorators here.
import logging
import signal
from exceptions import TimeoutError


class memoized(object):
    def __init__(self, func):
        self.cache = {}
        self.func = func
        
    def __call__(self, *arg):
        if arg in self.cache:
            return self.cache[arg]
        
        result = self.func(*arg)
        self.cache[arg]=result
        return result
        
class count_calls(object):
    counter_dict = {}
    
    def __init__(self, func):
        self.func = func
        count_calls.counter_dict[self.func.__name__] = 0
     
    def __call__(self, *args, **kwargs):
        count_calls.counter_dict[self.func.__name__] += 1
        return self.func(*args, **kwargs)
    
    def counter(self):
        return count_calls.counter_dict[self.func.__name__]
    
    @classmethod
    def counters(cls):
        return cls.counter_dict
        
    @classmethod
    def reset_counters(cls):
        cls.counter_dict = {}
        

class timeout(object):
    def __init__(self, seconds=2):
        self.seconds = seconds
        
    def __call__(self, func):
        def time_wrap(*arg, **kwargs):
            '''
            tstart = time.time()
            result = func(*arg, **kwargs)
            tend = time.time()
            if tend - tstart> self.seconds:
                self._handle_timeout()
                #raise TimeoutError('Function call timed out')
            else:
                return result
            '''
            signal.signal(signal.SIGALRM, self._handle_timeout)
            signal.alarm(self.seconds)
            result = func(*arg, **kwargs)
            signal.alarm(0)
            return result
            
        return time_wrap
                
    def _handle_timeout(self, signum, frame):
        raise TimeoutError('Function call timed out')
        
def debug(logger =  None):
    
    def debug_decor(func):
        if not logger:
            debug_log = logging.getLogger(func.__module__)
        else:
            debug_log = logger
            
        def dwrap(*arg, **kwarg):      
            debug_log.debug('Executing "{}" with params: {}, {}'.format(func.__name__, arg, kwarg))
            res = func(*arg, **kwarg)
            #res = reduce((lambda x,y: x+y), arg)
            debug_log.debug('Finished "{}" execution with result: {}'.format(func.__name__, res))
            return res
        return dwrap
    return debug_decor
    
    

    