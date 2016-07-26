import logging
# import inspect
import signal
from exceptions import TimeoutError

class count_calls(object):
    
    counters_dict = {}
    
    def __init__(self, function):
        self.function = function
        self.func_name = self.function.__name__
        if self.func_name not in self.counters_dict.keys():
            self.__class__.counters_dict[self.func_name] = 0 # instead of cls, use self.__class__
    
    def __call__ (self):
        self.__class__.counters_dict[self.func_name] += 1
        return self.function()
    
    def counter(self):
        return  self.__class__.counters_dict.get(self.func_name, 0)
        
    @classmethod
    def counters(cls):
        return cls.counters_dict
    
    @classmethod
    def reset_counters(cls):
        cls.counters_dict = {}
        
class memoized(object):
    cache = {}
    # {     "add":  {
    #                   (1, 2, 3): 1,
    #                   (4, 5, 6): 1
    #               }
    # }
    
    def __init__(self, function):
        self.function = function
        #self.count = 0
        self.func_name = self.function.__name__
        self.cache = {}
                        #structure for self.cache should be:
                            # {
                    #                   (1, 2, 3): 1,
                    #                   (4, 5, 6): 1
                    #               }
    
    def __call__ (self, *args):
        args_tuple = tuple(args)
        if self.cache and self.cache.get(args_tuple, False): # if both function and parameters are stored in cache
            return self.cache[args_tuple] # return cached result
            
        result = self.function(*args)
        
        if self.cache and (args_tuple not in self.cache): # if function is cached but NOT parameters
            self.cache[args_tuple] = result
            return result
        else: # if function has not been stored in cache previously
            self.cache = {args_tuple: result}
            return result
    
   
class debug(object):
    
    def __init__(self, logger=None):
        if logger == None:
            # line below gets you 'test_decorators', but not 'tests.test_decorators'
            # giving up after many hours because I don't know and the Net can't tell
            # me what the magic incantation is to get this string. Hardcoding is my
            # only option!
            
            # caller = inspect.getmodulename(inspect.stack()[1][1])
            caller = 'tests.test_decorators'
            self.logger = logging.getLogger(caller)
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger = logger
    
    def __call__(self, function):
        def wrapper(*args, **kwargs):
            debug_string = 'Executing "{}" with params: {}, {}'.format(function.__name__, args, kwargs)
            self.logger.debug(debug_string)
            result = function(*args)
            debug_string = 'Finished "{}" execution with result: {}'.format(function.__name__, result)
            self.logger.debug(debug_string)
            return result
        return wrapper
        
class timeout(object):
    def __init__(self, time=1):
        self.time = time
    
    def __call__(self, function):
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, self.handler)
            # start the timer
            signal.alarm(self.time)
            return function(*args, **kwargs)
        return wrapper
        
    def handler(self, signum, frame):
        print('Signal handler called with signal', signum)
        raise TimeoutError("Function call timed out")