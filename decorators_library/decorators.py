import logging

#time out dec




# debug:
class debug():
    def __init__(self, logger=None):
        self.logger = logger
        logging.basicConfig(
        level=logging.DEBUG,
        format='%(name)s %(levelname)s %(message)s'
        # filename=logging_file,
        # filemode='w',
        )
    def __call__(self,f):
        if not self.logger:
            self.logger = logging.getLogger(f.__module__)
        def new_func(*args, **kwargs): #*args, **kwargs):
            self.logger.debug('Executing "{}" with params: {}, {}'.format(f.__name__,args, kwargs))
            result = f(*args,**kwargs)
            self.logger.debug('Finished "{}" execution with result: {}'.format(f.__name__,result))
            return result
        return new_func



# count calls
class count_calls():
    counters_cache = {} #Class global
    
    def __init__(self, f):
        self.count = 0
        self.f = f
        self.key = f.__name__
        self.cache = {self.key:0}
        count_calls.counters_cache = self.cache
        
    def __call__(self,*args):
        if self.key in self.cache:
            self.cache[self.key] += 1
        count_calls.counters_cache[self.key] = self.counter()
        return self.f(*args)
        
    def counter(self):
        return self.cache[self.key]
    
    # Used to refer to class global
    @classmethod
    def counters(cls):
        return cls.counters_cache
        
    @classmethod
    def reset_counters(cls):
        cls.counters_cache = {}
        return


# memoized
class memoized():
    def __init__(self, function):
        self.function = function
        self.cache = {} #This should be in the following structure {arg:result}
    def __call__(self, *args):
        if args in self.cache:
            return self.cache[args]
        else:
            result = self.function(*args)
            self.cache[args] = result
            return result