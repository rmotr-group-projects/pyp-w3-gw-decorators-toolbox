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
    
    
    

	
class memoized():
    
    def __init__(self, func):
        self.func = func
        self.cache = {}
     
    #Have the same signature as the original func that is being decorated    
    def __call__(self, *args):
        if args not in self.cache:
            result = self.func(*args)
            self.cache[args] = result
            return result
        else:
            return self.cache[args]
            
            
class count_calls():
    
    #class variable to hold func and its call values
    result_data = {}
    
    def __init__(self,func):
        self.count = 0
        self.func = func
        
         
    
       
    def counter(self):
        """Sets the current count value to function name in class variable (result_data)"""
        count_calls.result_data[self.func.__name__] = self.count
        return self.count 
        
    @classmethod
    def counters(cls):
        return count_calls.result_data
        
        
    @classmethod
    def reset_counters(cls):
        count_calls.result_data = {}
    
    def __call__(self):
        #Increase the value of count every time the decorator is called
        self.count+=1
        return self.func()
        
        
        
import logging
def debug(logger=None):
    def func_wrapper(func):
        def inner_wrapper(*args):
            
            result = func(*args)
            
            logging.basicConfig()
            if not logger:
                
                c_logger = logging.getLogger('tests.test_decorators') #Remove hard coded names
                c_logger.setLevel('DEBUG')
                c_logger.debug('Executing "{}" with params: {}, {}'.format(func.__name__, args,"{}"))
                c_logger.debug('Finished "{}" execution with result: {}'.format(func.__name__, result))
                return result
                
            else:
                c_logger = logging.getLogger('test_decorators.{}'.format(logger))
                c_logger.setLevel('ERROR')
                
                return result
                
                
                
            
        return inner_wrapper
    return func_wrapper
    
    
    

def is_authenticated(func):
    #mock database
	database = ['Jhon', 'Santiago', 'Martin']
	def func_wrapper(username):
		if username in database:
			return func(username)
		else:
			return "User not authenticated. Please register"
	return func_wrapper
    
    
    
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
	

# def count_calls(func):
#     count_calls.count = 0
#     result_dict = {}
#     counter = 1
    
#     def counter():
#         count_calls.count+=1
#         return count_calls.count
        
#     def counters():
#         if func.__name__ not in result_dict:
#             result_dict[func.__name__] = counter()
#         else:
#             result_dict[func.__name__]+=1
#         return result_dict
        
#     def wrapper():
#         return func()
#     return wrapper
        
        
    
        
        