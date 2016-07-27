# implement your decorators here.
import time
import logging 
from decorators_library.exceptions import TimeoutError
from collections import defaultdict

def timeout (limit) :
    def to_decorate(f) :
        def inner_func(*args, **kwargs):
            begin = time.time()
            # function goes here 
            inner_output = f(*args, **kwargs)
            end = time.time()
            time_difference = end - begin
            if time_difference > limit :
                raise TimeoutError("Function call timed out")
            else :
                return inner_output 
        return inner_func
    return to_decorate



class count_calls (object) :
    # use this class attribute to keep track of each func and its calls
    # we're using defaultdict because its easier and defaults to the int 0
    func_to_count_dict = defaultdict(int)
    
    def __init__ (self, f, *args, **kwargs) :
        self.func = f
        self.func_name = f.__name__
        
    def __call__ (self, *args, **kwargs) :
        # going to directly mutate the class attribute!! :o 
        # dangerzone ! 
        count_calls.func_to_count_dict[self.func_name] +=1
        return self.func(*args, **kwargs)
    
    def counter(self) :
        # what does this do ?
        # it's an instance method that returns count of a particular func
        # looks like this : self.assertEqual(my_func.counter(), 4)
        return count_calls.func_to_count_dict[self.func_name]
    
    @classmethod
    def counters (cls) :
        # what does this do ? 
        # self.assertEqual(count_calls.counters(),
        #                 {'my_func': 3, 'my_other_func': 1})
        # it returns a dictionary 
        return dict(cls.func_to_count_dict)
        
    
    @classmethod    
    def reset_counters(cls) :
        cls.func_to_count_dict = defaultdict(int)
    



def debug (logger=None) :
    if logger is None:
        logging.basicConfig()
        debug_logger = logging.getLogger('tests.test_decorators')
        debug_logger.setLevel(logging.DEBUG)
        logger = debug_logger
    def to_decorate(f) :
        def inner_func(*args, **kwargs) :
            # started with params == ?
            logger.debug('Executing "{}" with params: {}, {}'.format(f.__name__, str(args), str(kwargs)))
        
            inner_output = f(*args, **kwargs)
            
            logger.debug('Finished "{}" execution with result: {}'.format(f.__name__, str(inner_output)))
            # ended with result == ?
            return inner_output
        return inner_func
    return to_decorate



class memoized(object) :
    def __init__ (self, f, *args) :
        self.func = f
        self.cache = defaultdict(int)
        
    def __call__ (self, *args) :
        curr_args = args
        
        if curr_args in self.cache.keys() :
            # lookup in cache dictionary
            return self.cache[curr_args]
        else : 
            # need to run the function
            output = self.func(*args)
            self.cache[curr_args] = output
            return output 
            