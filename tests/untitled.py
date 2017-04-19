# count calls
class count_calls():
    def __init__(self,f):
        self.count = 0
        self.f = f
        
    def __call__(self,*args):
        def new_f(*args):
            result = self.f(*args)
            self.count += 1
            print("self.count: ", self.count)
            return result
        return new_f

    def __iter__(self):
        return self

    def __next__(self):
        self.count += 1

    next = __next__
    
    def counter(self):
        print("I'm in the counter()")
        return self.count

@count_calls
def my_func(a,b):
    print('my func is called!')
    return a+b

# my_func = count_calls(my_func)

# iter(my_func(1,2))
my_func(1,2)
my_func(2,3)
my_func(3,4)
my_func(4,5)
print(my_func.counter())



# class only_numeric_arguments(object):
#     def __init__(self, integer, floats):
#         self.integer = integer
#         self.floats = floats

#     def __call__(self, f):
#         def new_f(a, b):
#             print("Executing %s" % f.__name__)
#             return f(a, b)

#         return new_f

# def add(a, b):
#     return a + b

# add = only_numeric_arguments(integer=True, floats=True)(add)
# print(add(2, 3))
