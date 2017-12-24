import functools

def inspect(function):
    @functools.wraps(function)
    def wrapper(x, y, operation='add'):
        if operation == 'add':
            result = function(x, y)
            print('{} invoked with {}, {}. Result: {}'.format(function.__name__, x, y, result))
        else:
            result = function(x, y, operation)
            print('{} invoked with {}, {}, operation={}. Result: {}'.format(function.__name__, x, y, operation, result))
        return result
    return wrapper

def memoized():
    pass

def count_calls():
    pass

def timeout():
    pass