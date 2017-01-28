import time
import signal
from exceptions import TimeoutError
import logging
from testfixtures import LogCapture
import resource

def timeout(seconds=1):
    """Useful to give functions a certain max time for execution.
    The decorator is suppose to track the execution time and raise
    and exception if the time exceeds given timeout range."""
    def decorator(fn):
        def _timeout_error(signum, frame):
            raise TimeoutError('Function call timed out')
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _timeout_error)
            signal.alarm(seconds)
            try:
                result = fn(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result
        return wrapper
    return decorator


class debug(object):
    """This decorator is suppose to debug the executions of the decorated
    function by logging a message before starting the execution including
    given params, and a second message after the execution is finished with
    the returned result."""
    
    before_msg = "Executing \"{}\" with params: {}, {}"
    after_msg = "Finished \"{}\" execution with result: {}"
    
    def __init__(self, func=None, logger=None):
        if logger == None:
            self.logger = logging
        else:
            self.logger = logger

    def __call__(self, fn):
        def wrapper(*args, **kwargs):
            self.logger.debug(self.before_msg.format(fn.__name__, args, kwargs))
            result = fn(*args)
            self.logger.debug(self.after_msg.format(fn.__name__, result))
            return result
        return wrapper


class count_calls(object):
    """Keeps track of how many times a certain function was called."""
    
    funcTotal = {}
    
    def __init__(self, function):
        self.function = function
        # self.call_count = 0
        self.funcTotal[self.function.__name__] = 0
        
    def __call__(self, *args, **kwargs):
        self.funcTotal[self.function.__name__] += 1
        # self.funcTotal[self.function.__name__] = self.call_count
        return self.function(*args, **kwargs)
        
    def counter(self):
        return self.funcTotal[self.function.__name__]
    
    @classmethod    
    def counters(cls):
        return cls.funcTotal
        
    @classmethod    
    def reset_counters(cls):
        cls.funcTotal = {}
        

class memoized(object):
    """This decorator should keep track of previous executions of the decorated
    function and the result of the invocations. If the decorated function is execution
    again using the same set of arguments sent in the past, the result must be
    immediately returned by an internal cache instead of re executing the same code again."""
    
    def __init__(self, function):
        self.cache ={}
        self.function = function
    
    def __call__(self, *args, **kwargs):
        if args not in self.cache:
            self.cache[args] = self.function(*args, **kwargs)
            return self.function(*args)
            
        elif args in self.cache:
            return self.cache[args]
        

class performance(object):
    """Get the time and mem before and after function execution."""
    
    msg = "Function '{}' took {} seconds and used {} of memory."
    
    def __init__(self, fn):
        self.f = fn

    def __call__(self, *args, **kwargs):
        
        #Before stat
        t_before = time.time()
        mem_before = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        
        self.f(*args, **kwargs) # Run function
        
        # After stats
        t_diff = round(time.time() - t_before,2)
        self.mem_diff = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss - mem_before
        
        return self.msg.format(
            self.f.__name__, 
            t_diff, 
            " ".join(self.mem_nice())
        )

    def mem_nice(self):
        m = self.mem_diff
        nm = 'B'
        if m > 1024:
            m, nm = m / 1024, 'KB'
        if m > 1024:
            m, nm = m / 1024, 'MB'
        return str(round(m,2)), nm


class type_decorator(object):
  """gives the type of all the arguemnts and the return of the function"""
  def __init__(self, function):
    self.function = function

  def __call__(self, *args):
    for arg in args:
      print ("{} is {}".format(arg, type(arg)))
    result = self.function(*args)
    print ("The result of the function '{}' is {}, {}".format(
        self.function.__name__, result, type(result)
        ))
    return result
    

def check_type(*types):
    """Checks the argument type and makes it mutable. (Ex: converts it into int or float)"""
    def decorator(function):
        def convert_type(*args, **kwargs):
            newArgs = []
            for (a, b) in zip(args, types):
                newArgs.append(b(a))
            return function(*newArgs, **kwargs)
        return convert_type
    return decorator
                
                
                
        