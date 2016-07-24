import logging
# implement your decorators here.

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
    pass
    # def init(self, function):
    #     self.logger = logging.getLogger(function.__name__)
    #     self.logger.setLevel(logging.DEBUG)
    
    # def __call__(self, *args, **kwargs):
    #     self.logger.debug('Executing {1} with params: {2}, {3}')
    #     pass
    #
    #
    #
    #
    #
    #
   