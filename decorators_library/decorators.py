import logging

# implement your decorators here.

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

# class only_numeric_arguments(object):
#     def __init__(self, integer, floats):
#         self.integer = integer
#         self.floats = floats
    
#     def __call__(self, f):
#         def new_f(a, b):
#             print("Executing %s" % f.__name__)
#             return f(a, b)
#         return new_f

# @only_numeric_arguments(integer=True, floats=True)
# def add(a, b):
#     return a + b
# print(add(2, 3))

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
        if self.logger == None:
            self.logger = logging.getLogger(f.__module__)
        def new_func(*args, **kwargs): #*args, **kwargs):
            self.logger.debug('Executing "{}" with params: {}, {}'.format(f.__name__,args, kwargs))
            result = f(*args,**kwargs)
            self.logger.debug('Finished "{}" execution with result: {}'.format(f.__name__,result))
            return result
        return new_func



# count calls




# memoized

