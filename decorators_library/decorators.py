# implement your decorators here.
def inspect(fn):
    def new_fn(*args, **kwargs):
        arg_list = []
        result = fn(*args, **kwargs)
        for arg in args:
            arg_list.append(str(arg))
        for kwarg in kwargs:
            arg_list.append(str(kwarg)+'='+kwargs[kwarg])
        print ('{} invoked with {}. Result: {}'.
               format(fn.__name__, ', '.join(arg_list), result))
        return result
    return new_fn


class count_calls(object):
    counter_cache = {}

    def __init__(self, fn):
        self.fn = fn
        count_calls.counter_cache[self.fn.__name__] = 0
        self.count = count_calls.counter_cache[self.fn.__name__]

    def __call__(self):
        count_calls.counter_cache[self.fn.__name__] += 1

    def counter(self):
        return count_calls.counter_cache[self.fn.__name__]

    @classmethod
    def reset_counters(cls):
        cls.counter_cache.clear()

    @classmethod
    def counters(cls):
        return cls.counter_cache


def timeout(fn):
    pass


class memoized(object):
    
    def __init__(self, fn):
        self.fn = fn
        self.cache = {}

    def __call__(self, *args, **kwargs):
        def cach_check(*args, **kwargs):
            try:
                return self.cache[args]
            except KeyError:
                self.cache[args] = self.fn(*args, **kwargs)
                return self.cache[args]
        return cach_check(*args, **kwargs)
