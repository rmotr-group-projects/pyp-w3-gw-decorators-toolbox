# implement your decorators here.
import signal
import time
from exceptions import FunctionTimeoutException

def inspect(fn):
    def operation(*args, **kwargs):
        op = fn.__name__
        argstrng = ""
        if kwargs:
            kw = True
        else:
            kw = False
            
        for a in range(len(args)):
            argstrng += str(args[a])
            if a < len(args) - 1:
                argstrng += ', '

        if kw:
            argstrng += ', '
            for key, value in kwargs.items():
                argstrng += str(key) + '=' + str(value)
                
            argstrng += '.'
        else:
            argstrng.rstrip()
            argstrng += '.'
                
        result = fn(*args, **kwargs)
        print "{o} invoked with {i} Result: {r}".format(o = op, i = argstrng, r = result)
        return fn(*args, **kwargs)
    return operation
    


class timeout(object):
    def __init__(self, value, exception=FunctionTimeoutException):
        self.value = value
        self.exception=exception
        
    def __call__(self, fn):
        def wrapped(*args, **kwargs):
            def receive_alarm(signum, stack):
                raise self.exception('Function call timed out')

             
            signal.signal(signal.SIGALRM, receive_alarm)
            signal.alarm(self.value)
            
            return fn(*args, **kwargs)
        return wrapped



class count_calls(object):
    _counts = {}
    
    def __init__(self, fn):
        self.fn = fn
        count_calls._counts.setdefault(self.fn.__name__, 0)

    def __call__(self):
        count_calls._counts[self.fn.__name__] += 1
            
           
    @classmethod        
    def reset_counters(cls):
        cls._counts = {}

    @classmethod
    def counters(cls):
        return cls._counts
    
    def counter(self):
        return count_calls._counts[self.fn.__name__]
    
            
class memoized(object):
    def __init__(self, fn):
        self.stored = {}
        self.fn = fn
    
    def __call__(self, a, b):
        def wrapped(a, b):
            
            t = (a, b)
            
            
            if t in self.stored:
                return self.stored[t] 
                
            result = self.fn(a, b)
            
            self.stored[t] = result
            
            return self.fn(a, b)
            
        return wrapped(a, b)
    
    @property
    def cache(self):
        #returns cached values
        return self.stored






        