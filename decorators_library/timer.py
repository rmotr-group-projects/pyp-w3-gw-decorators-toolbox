# decorator template
# def decorator(func):
#     def new_func(a,b):
#         print("print something if you wish")
#         return func(a,b)
#     return new_func

# @decorator
# def func(a,b):
#     return a + b
# # same thing as
# func = decorator(func)
# print(func(1,3)


import time

def timer(f):
    def new_t(*args, **kwargs):
        start = time.time()
        result = f(*args,**kwargs)
        end = time.time()
        total_time = end-start
        return total_time
    
@timer    
def add_me(a,b):
    return a+b

print add_me(2,3)