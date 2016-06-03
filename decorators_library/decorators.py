# implement your decorators here.
import time
# from . import TimeoutError
class TimeoutError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

# def timeout(func, t):
#     start_time = time.time()
#     def new_func(t):
#         if time.time() - start_time > t:
#             res = func()
#             raise TimeoutError("Function call timed out")
#         return res
#     return new_func

class timeout(object):
    def __init__(self, t):
        self.t = t
    
    def __call__(self, func):
        start_time = time.time()
        func()
        total_time = time.time() - start_time
        if total_time > self.t:
            raise TimeoutError("Function call timed out")
        return func
        
        
class memoized(object):
    def __init__(self, f):
        self.f = f
        self.cache = dict()
        
    def __call__(self, a, b):
        if (a,b) in self.cache:
            return self.cache[(a,b)]
        res = self.f(a,b)
        self.cache[(a,b)] = res
        return res
        
'''
def memoized(f):
    cache = dict()
    #setattr(memoized, "cache", {})
    def new_f(a, b):
        if (a,b) in cache:
            return cache[(a,b)]
        res = f(a,b)
        cache[a,b] = res
        return res
    return new_f
'''
        
class count_calls(object):
    dict_data = {}
    def __init__(self, f):
        self.f = f
        self.count = 0
        count_calls.dict_data[self.f.__name__] = self.count
        
    def __call__(self):
        self.count += 1
        count_calls.dict_data[self.f.__name__] = self.count
        return self.f
   
    def counter(self):
        return self.count
    
    @classmethod
    def counters(cls):
        return cls.dict_data
        
    @classmethod
    def reset_counters(cls):
        cls.dict_data = {}
        
     
# @timeout(2)
# def greg_test():
#     time.sleep(1)
#     print("yoyoyoyo")
# greg_test()
