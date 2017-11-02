# implement your decorators here.
def timeout():
    pass


def memoized():
    pass


def count_calls():
    pass


def inspect(fn):
    def wrapper(*args, **kwargs):
        formatted_kwargs = []
        for key, value in kwargs.items():
            formatted_kwargs.append('{}={}'.format(key, value))
        all_args = list(args) + formatted_kwargs
        all_args = ', '.join(str(arg) for arg in all_args)
        result = fn(*args, **kwargs)
        print('{} invoked with {}. Result: {}'.format(fn.__name__, all_args,
                                                      result))
        return fn(*args, **kwargs)
    return wrapper
