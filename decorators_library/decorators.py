import signal
import logging

# implement your decorators here.
class count_calls(object):
    """
    Keeps track of how many times certain function was called:
    """
    # dictionary to track count of all decorated functions
    _counters = {}
    
    def __init__(self, fn):
        self._counter = 0
        self.fn = fn
        count_calls._counters[self.fn.__name__] = 0
        
    def counter(self):
        return self._counter
        
    def __call__(self):
        self._counter += 1
        try:
            self._counters[self.fn.__name__] += 1
        except KeyError:
            self._counters[self.fn.__name__] = 1
        return self.fn()

        
    @classmethod
    def counters(cls):
        return cls._counters
        
    @classmethod
    def reset_counters(cls):
        cls._counters = {}
        
class memoized(object):
    """
    This decorator should keep track of previous executions of the decorated 
    function and the result of the invokations. If the decorated function is 
    execution again using the same set of arguments sent in the past, 
    the result must be immediately returned by an internal cache instead 
    of re executing the same code again. 
    """
    def __init__(self, fn):
        self.cache = {}
        self.fn = fn
    
    def __call__(self, *args):
        self.cache[args] = self.fn(*args)
        return self.fn(*args)
    
class timeout(object):
    """
    Useful to given functions a certain max time for execution. 
    The decorator is suppose to track the execution time
    and raise and exception if the time exceeds given timeout range. 
    """
    def __init__(self, secs):
        self.secs = secs
    
    def __call__(self, fn):
        def _handle_timeout(signum, frame):
            raise TimeoutError('Function call timed out')
        
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(self.secs)
            return fn(*args, **kwargs)
        return wrapper
        
class debug(object):
    """
    This decorator is suppose to debug the executions of the decorated function
    by logging a message before starting the execution including given params, 
    and a second message after the execution is finished 
    with the returned result. 
    """
    def __init__(self, logger=None):
        self.logger = logger
    
    def __call__(self, fn):
        def wrapper(*args, **kwargs):
            if not self.logger:
                self.logger = logging.getLogger(fn.__module__)
            self.logger.debug('Executing "{}" with params: {}, {}'.format(fn.__name__, args, kwargs))
            self.logger.debug('Finished "{}" execution with result: {}'.format(fn.__name__, fn(*args, **kwargs)))
            return fn(*args, **kwargs)
        return wrapper
            
        