from .exceptions import FunctionTimeoutException

import signal
import time

def inspect(op):
    def opx(*args, **kwargs):
        #result = x + y 
        args_ = ', '.join([str(arg) for arg in args])
        result = op(*args, **kwargs)
        if len(kwargs) == 0:
            print("{} invoked with {}. Result: {}".format(op.__name__,args_,result)) #  {}, {}. Result: {} , x, y, result))
        else:
            kwargs_ = ', '.join([value for key, value in kwargs.items()])    
            #print(kwargs_)
            print("{} invoked with {}, operation={}. Result: {}".format(op.__name__,args_,kwargs_,result)) #  {}, {}. Result: {} , x, y, result))
        #print(op(*args, **kwargs))    
        return op(*args, **kwargs)
    return opx
        
# @inspect 
# def my_add(a,b, operation = 'add'):
#     #print('I am here')
#     return a + b 

#print(my_add(1,2, operation = 'subtract'))

'''
calculate invoked with 7, 2. Result: 9",
"calculate invoked with 9, 6, operation=subtract. Result: 3
'''

# def inspect(op):
#     def opx(x,y):
#         result = x + y 
#         print("{} invoked with {}, {}. Result: {}".format(op.__name__, x, y, result))
#         return op(x,y)
#     return opx
        
# @inspect 
# def my_add(a,b):
#     #print('I am here')
#     return a + b 






class count_calls(object):
    
    func_counter_dict = {}
    #_counter = 0
    
    def __init__(self,original_function):
        self.original_function = original_function
        self.func_counter = 0
        count_calls.func_counter_dict[self.original_function.__name__] = self.func_counter
   
    def __call__(self):
        '''In the class based implementation you do not need the func wrapper, __call__ works as the wrapper
         "and you have to execute the inner function, you only need wrapepr function to pass arguments to decorators''' 
        self.func_counter += 1
        print(self.original_function.__name__)
        count_calls.func_counter_dict[self.original_function.__name__] = self.func_counter
        return self.original_function()
    
    def counter(self):
        #print(self.original_function.__name__)
        return count_calls.func_counter_dict[self.original_function.__name__]
   
    @classmethod    
    def reset_counters(cls):
        count_calls.func_counter_dict = {} 
    
    @classmethod    
    def counters(cls):
        return count_calls.func_counter_dict






def timeout(max_time , exception = FunctionTimeoutException):  # u always know the number of arguments your decorator will take
    def receive_alarm(signum, stack):
        raise exception('Function call timed out')
        print('Alarm :', time.ctime())

    def wrapper(func):
        def func_wrapper(*args, **kwargs): # args and kwargs is for the function arguments. the function can take any number of args
            #write your code here
            print(max_time)
            signal.signal(signal.SIGALRM, receive_alarm) # alarm will raise after max_time, first line is listening to second line
            signal.alarm(max_time)
            t1 = time.time()
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            t2 = time.time() - t1
            #print('{} rans for {} secs'.format(func.__name__, t2))
            return result     
        return func_wrapper
    return wrapper    
    
# @timeout(5,FunctionTimeoutException)
# def very_slow_function():
#     time.sleep(1)
#     print('I am here')

# very_slow_function()
# #time.sleep(10)




class memoized(object):
    
    def __init__(self, func):
        self.func = func
        self.cache = {}
        #print('I am here')
   
    def __call__(self,x,y):
        if (x,y) in self.cache:
            print('{} was not executed for {} {} result was returned from internal cache'.format(self.func.__name__, x , y ))
            print(self.cache)
            return self.cache[(x,y)]
        else:
            self.cache[(x,y)] = self.func(x,y)
            print('{} was executed for {} {} result is {}'.format(self.func.__name__, x , y,self.func(x,y) ))
            #print('I am Here')
            return self.func(x,y)

# @memoized
# def add(a, b):
#     return a + b

# add(1,2)   #, 3
# add(2,3)  #, 5
# print(add.cache)  #, {(1, 2): 3, (2, 3): 5})
# print(add(1,2))  #, 3)
# print(add.cache) #, {(1, 2): 3, (2, 3): 5})
# add(3,4)  #, 7)
# print(add.cache) #, {(1, 2): 3, (2, 3): 5, (3, 4): 7})



'''
def memoized(op):
    op.cache = {}
    def opx(x,y):
        if (x,y) in op.cache:
            print('{} was not executed for {} {} result was returned from internal cache'.format(op.__name__, x , y ))
            print(op.cache)
            return op.cache[(x,y)]
        else:
            op.cache[(x,y)] = op(x,y)
            print('{} was executed for {} {} result is {}'.format(op.__name__, x , y,op(x,y) ))
            return op(x,y)
    return opx

# @memoized
# def add(a, b):
#     return a + b

# print(add(1,2))   #, 3
# print(add(2,3))  #, 5
# print(add.cache)  #, {(1, 2): 3, (2, 3): 5})
# print(add(1,2))  #, 3)
# # print(add.cache) #, {(1, 2): 3, (2, 3): 5})
# # add(3,4)  #, 7)
# # print(add.cache) #, {(1, 2): 3, (2, 3): 5, (3, 4): 7})
'''



def debug(op):
    def add(x, y):
        print("Executing '{}' with params: ({}, {}), {{}}".format(op.__name__, x, y))
        return x + y 

    def opx(x,y):
        #result = add(x,y)
        print("Executing '{}' with params: ({}, {}), {{}}".format(op.__name__, x, y))
        print("Finished '{}' execution with result: {}".format(op.__name__, op(x,y)))
        return op
    return opx
        
# @debug
# def my_add(a,b):
#     return  a + b

# res = my_add(1, 2)
# #print(res)





