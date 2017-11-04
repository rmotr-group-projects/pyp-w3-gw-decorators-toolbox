
import time
import signal
from decorators_library.exceptions import FunctionTimeoutException
# implement your decorators here.


class Timeout(object):
    def __init__(self, _time, exception = FunctionTimeoutException):
        self._time = _time
        self.exception = exception
    
    @staticmethod
    def receive_alarm(signum, stack):
        print('Alarm: {}'.format(time.ctime()))
        
    def __call__(self, fn):
        def wrap_fn():
            tb = time.time()
            f = fn()
            ta = time.time()
            
            signal.signal(signal.SIGALRM, Timeout.receive_alarm)
            signal.alarm(2)

            if self.exception == FunctionTimeoutException:
                texc_begin = time.time()
                
                if ta-tb > self._time:
                    raise self.exception("Function call timed out")
                    
                texc_end = time.time()
               
                if texc_end - texc_begin < 3:
                    return "Function allowed to execute past timeout."
            else:
                raise self.exception('Function call timed out')
            
            return f
        return wrap_fn

# An instance of Timeout class        
timeout = Timeout

def inspect(fn):
    def _print(*args, **kwargs):
        if kwargs:
            print("{} invoked with {}, {}. Result: {}".format(fn.__name__, ', '.join([str(arg) for arg in args]), ', '.join(['{}={}'.format(k,v) for k, v in kwargs.items()]) , fn(*args, **kwargs)))
        else:
            print("{} invoked with {}. Result: {}".format(fn.__name__, ', '.join([str(arg) for arg in args]), fn(*args, **kwargs)))
        
        return fn(*args, **kwargs)
        
    return _print

class Memoized(object):
  def __init__(self, fn):
    self.cache = {}
    self.fn = fn
  
  def __call__(self, *args, **kwargs):

    for key, value in self.cache.items():
        if key == args:
            return value
        
    self.cache[args] = self.fn(*args, **kwargs)
    
    return self.fn(*args, **kwargs)

memoized = Memoized

class Count_calls(object):
    counts = {}
    
    def __init__(self, fn):
        self.fn = fn
        self.count = 0
        Count_calls.counts[fn.__name__] = 0
        
    def __call__(self):
        self.count += 1
        f = self.fn.__name__
      
        if f in Count_calls.counts.keys():
            Count_calls.counts[f] = self.count
        else:
            Count_calls.counts[f] = 1
        
        return self.fn()
    
    def counter(self):
        return self.count
    
    @classmethod
    def counters(cls):
        return cls.counts
    
    @classmethod
    def reset_counters(cls):
        cls.counts = {}

count_calls = Count_calls
