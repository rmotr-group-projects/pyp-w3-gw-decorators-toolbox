class TimeoutError(Exception):
    def __init__(self):
        self.message = 'Function call timed out'
        
    def __str__(self):
        return self.message