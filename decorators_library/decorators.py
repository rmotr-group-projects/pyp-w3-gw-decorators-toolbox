# implement your decorators here.

class count_calls(object):
    
    counters_dict = {}
    
    def __init__(self, function):
        self.function = function
        #self.count = 0
        self.func_name = self.function.__name__
    
    def __call__ (self):
        # if not self.count:
        if self.func_name not in self.counters_dict.keys():
            self.__class__.counters_dict[self.func_name] = 0 # instead of cls, use self.__class__
        self.__class__.counters_dict[self.func_name] += 1
        return self.function()
    
    def counter(self):
        return  self.__class__.counters_dict[self.func_name]
        
    @classmethod
    def counters(cls):
        return cls.counters_dict
    
    @classmethod
    def reset_counters(cls):
        cls.counters_dict = {}