# implement your decorators here.
import time
from .exceptions import TimeoutError

def timeout(stop_by):
    def get_func(func):
        def func_wrapper():
            
            start = time.time()
            result = func()
            end = time.time()
            difference = int(end - start)
            
            if difference > stop_by:
                raise TimeoutError('Function call timed out')
            return result
        return func_wrapper
    return get_func
    
    
    
# def memoized(original_function):
# 	original_function.cache = {}
	
# 	def func_wrapper(*args):
# 		result = original_function(*args)
# 		original_function.cache[args] = result
# 		if args not in original_function.cache:
# 			original_function.cache[args] = result
# 		else:
# 			#Return the value from internal cache
# 			return original_function.cache[args]
# 		return result
# 	return func_wrapper
	
	
class memoized():
    
    def __init__(self, func):
        self.func = func
        self.cache = {}
        
    def __call__(self, *args):
        if args not in self.cache:
            result = self.func(*args)
            self.cache[args] = result
            return result
        else:
            return self.cache[args]