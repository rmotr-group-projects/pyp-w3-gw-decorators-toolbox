import signal
import functools
import logging
import collections

from .exceptions import TimeoutError

# The first decorator

def timeout(seconds):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError('Function call timed out')
            
        signal.signal(signal.SIGALRM, _handle_timeout)
        signal.alarm(seconds)
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result
            
        return wrapper
    return decorator
    

# The second decorator

class debug(object):
    
    first_message = 'Executing "{}" with params: {}, {}'
    second_message = 'Finished "{}" execution with result: {}'
    
    def __init__(self, logger=None):
        self.logger = logger
        
    def __call__(self, func):
        
        if not self.logger:
            logging.basicConfig()
            self.logger = logging.getLogger(func.__module__)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            self.logger.debug(self.first_message.format(func.__name__, args, kwargs))
            result = func(*args, **kwargs)
            self.logger.debug(self.second_message.format(func.__name__, result))
            return result
        return wrapper


class count_calls(object):

    # This decorator should keep track of different function calls,
    # i.e. it needs some kind of 'global' container

    global_container = dict()

    def __init__(self, func):
        self.counter = 0
        self.func = func
        count_calls.global_container[func] = self

    def __call__(self, *args, **kwargs):
        self.counter += 1
        return self.func(*args, **kwargs)

    def counter(self):
        return count_calls.global_container.counter()
        

class count_calls(object):
    global_container = dict()

    def __init__(self, func):
        self.func = func
        self.calls_recorded = 0
        count_calls.global_container[func] = self

    def __call__(self, *args, **kwargs):
        self.calls_recorded += 1
        return self.func(*args, **kwargs)

    def counter(self):
        return count_calls.global_container[self.func].calls_recorded

    @classmethod
    
    # I really struggled with this part. After one day thinking about it,
    # I gave up. I had to look into your solutions.
    
    def counters(c):
        return dict([(f.__name__, c.global_container[f].calls_recorded)
                     for f in c.global_container])

    @classmethod
    def reset_counters(c):
        c.global_container = dict()
        

class memoized(object):

    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        
        if not isinstance(args, collections.Hashable):
            return self.func(*args)

        if args in self.cache:
            return self.cache[args]

        else:
            result = self.func(*args)
            self.cache[args] = result
            return result
            
def minimum_runtime(seconds):
    '''This decorator slows down the execution of a given function.'''
    
  def decorated_function(func):
    
    def wrapper(*args, **kwargs):
      start = time.time()
      result = func(*args, **kwargs)
      runtime = time.time() - start
    
      if runtime < seconds:
        time.sleep(seconds - runtime)
    
      return result
    
    return wrapper
  
  return decorated_function
  
  
'''
For the first time during the course, I was not able to complete
the assignment. Unfortunately, this time it was for personal reasons
I didn't expect.

My apologies.
Michal
'''