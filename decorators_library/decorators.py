# implement your decorators here.
class count_calls(object):
    cls_counter = {}
    
    def __init__(self, func):
        self.func = func
        self.count = 0
        count_calls.cls_counter[func.__name__] = 0
        

    def __call__(self, *args, **kwargs):
        self.count += 1
        count_calls.cls_counter[self.func.__name__] = self.count
        return self.func(*args, **kwargs)
        
    def counter(self):
        return self.count
        
    @classmethod
    def counters(cls):
        return cls.cls_counter
        
    @classmethod
    def reset_counters(cls):
        cls.cls_counter.clear()

class memoized(object):
    def __init__(self, func):
        self.func = func
        self.cache = {}
        
    def __call__(self, *args):
        if args in self.cache:
            return self.cache[args]
        else:
            value = self.func(*args)
            self.cache[args] = value
            return value