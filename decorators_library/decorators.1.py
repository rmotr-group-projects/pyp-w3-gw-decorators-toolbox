# implement your decorators here.
#inspect


def inspect(op):
    def opx(x,y):
        result = x + y 
        print("{} invoked with {}, {}. Result: {}".format(op.__name__, x, y, result))
        return result
    return opx
        
@inspect 
def my_add(a,b):
    return a + b 


def memoized(op):
    cache = {}
    def opx(x,y):
        if (x,y) in cache:
            print('{} was not executed for {} {} result was returned from internal cache'.format(op.__name__, x , y ))
            return cache[(x,y)]
        else:
            cache[(x,y)] = x + y
            print('{} was executed for {} {} result is'.format(op.__name__, x , y, ))
            return x + y
    return opx

@memoized
def add(a, b):
    return a + b

class count_calls(object):
    def __init__(self,original_function):
        self._counter = 0
        self.original_function = original_function
        
    def __call__(self):
        def func_wrapper():
            self._counter += 1
            print(self._counter)
            return self.original_function()
        return func_wrapper
        
    def counter(self):
        return self._counter

@count_calls
def my_func():
    print('I am here')





#Keeps track of how many times certain function was called. Example:


my_func()
my_func()
my_func()
my_func()
#print(my_func.counter())

