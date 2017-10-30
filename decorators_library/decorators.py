import signal
from .exceptions import FunctionTimeoutException

def inspect(fn):
    def new_fn(*args, **kwargs):
        
        s1 = "{} invoked with {}, {}".format(fn.__name__, args[0], args[1])
        if (len(kwargs) > 0):
            s1 += ", operation={}. Result: {}".format(
                  kwargs['operation'], 
                  fn(*args, **kwargs))
        else:   
            s1 += ". Result: {}".format(fn(*args))
        
        print(s1)
        return fn(*args, **kwargs)
    
    return new_fn

class timeout(object):
    def __init__(self, duration, exception=FunctionTimeoutException):
        self.duration = duration
        self.exception = exception
    
    def handler(self, signum, frame):
        raise self.exception("Function call timed out")
    
    def __call__(self, fn):
        def new_fn(*args, **kwargs):
            # Set the signal handler and a x-second alarm
            signal.signal(signal.SIGALRM, self.handler)
            signal.alarm(self.duration)
            res = fn(*args, **kwargs)
            # disable alarm
            signal.alarm(0)
            return res
        return new_fn

class count_calls(object):
    function_dict = {}
 
    def __init__(self, fn):
        self.fn = fn
        self.function_dict[self.fn.__name__] = 0
    
    @classmethod
    def counters(cls):
        return cls.function_dict
        
    @classmethod
    def reset_counters(cls):
        cls.function_dict = {}
        
    def counter(self):
        return self.function_dict[self.fn.__name__]
    
    def __call__(self, *args, **kwargs):
        self.function_dict[self.fn.__name__] += 1
        return self.fn(*args, **kwargs)
        
class memoized(object):
    
    global cache_dict
    cache_dict = {}
    
    def __init__(self, fn):
        self.fn = fn
    
    def __call__(self, *args, **kwargs):
        items = []
        for arg in args:
            items.append(arg)
        items = tuple(items)
        
        if cache_dict.get(items):
            return cache_dict[items]
        cache_dict[items] = self.fn(*args, **kwargs)
        return cache_dict[items]
        
    @property
    def cache(self):
        return cache_dict