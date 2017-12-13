from .exceptions import FunctionTimeoutException
import signal

class timeout(object):
    def __init__(self, duration, exception=FunctionTimeoutException):
        self.duration = duration
        self.exception = exception
    
    def alert(self, signum, frame):
        raise self.exception("Function call timed out!")
    
    def __call__(self, fun):
        def timeout_function(*args, **kwargs):
            signal.signal(signal.SIGALRM, self.alert)
            signal.alarm(self.duration)
            result = fun(*args, **kwargs)
            signal.alarm(0)
            return result
        return timeout_function

def inspect(fun):
    def inspect_function(*args, **kwargs):
        string = "{} invoked with {}, {}".format(fun.__name__, args[0], args[1])
        if (len(kwargs) > 0):
            string += ", operation={}. Result: {}".format(
                  kwargs['operation'], 
                  fun(*args, **kwargs))
        else:   
            string += ". Result: {}".format(fun(*args))
            
        print(string)
        return fun(*args, **kwargs)
        
    return inspect_function

class count_calls(object):
    total_count = {}
 
    def __init__(self, fun):
        self.fun = fun
        self.total_count[self.fun.__name__] = 0
    
    @classmethod
    def counters(cls):
        return cls.total_count
        
    @classmethod
    def reset_counters(cls):
        cls.total_count = {}
        
    def counter(self):
        return self.total_count[self.fun.__name__]
    
    def __call__(self, *args, **kwargs):
        self.total_count[self.fun.__name__] += 1
        return self.fun(*args, **kwargs)

class memoized(object):
    
  def __init__(self,fun):
      self.fun = fun
      self.cache = {}

  def __call__(self,*args):
    if args in self.cache:
        return self.cache[args]
    result = self.fun(*args)
    print ("Not using cached value")
    self.cache[args] = result
    return result