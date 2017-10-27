import signal

class FunctionTimeoutException(Exception):
    pass

# implement your decorators here.
def inspect(fn):
    def new_add(a, b, **kwargs):
        result = fn(a, b, **kwargs)
        if not kwargs or kwargs['operation'] == 'add':
            extra_text = ''
        else:
            extra_text = ', operation={}'.format(kwargs['operation'])
        print('{} invoked with {}, {}{}. Result: {}'.format(fn.__name__,a,b,extra_text,result))
        return result
    return new_add
    
class timeout(object):
    def __init__(self, timeout, exception=FunctionTimeoutException):
        self.timeout = timeout
        self.exception = exception
        
    def receive_alarm(self, signum, stack):
        raise self.exception('Function call timed out')
    
    def __call__(self, fn):
        def new_fn(*args, **kwargs):
            signal.signal(signal.SIGALRM, self.receive_alarm)
            signal.alarm(self.timeout)
            result = fn(*args, **kwargs)
            signal.alarm(0)
            return result
        return new_fn

def memoized():
    pass

class count_calls(object):
    glob_count = {}
    
    def __init__(self, fn):
        self.ind_count = 0
        self.fn = fn
        if not self.glob_count.get(self.fn.__name__):
            self.glob_count[self.fn.__name__] = 0
        
    def __call__(self):
        self.glob_count[self.fn.__name__] += 1
        self.ind_count += 1
        return self.fn()
    
    def counter(self):
        return self.ind_count

    @classmethod
    def counters(cls):
        return cls.glob_count 

    @classmethod
    def reset_counters(cls):
        cls.glob_count = {}
 