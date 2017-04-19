class TimeoutError(Exception):
    def __init__(self, value='Function call timed out'):
        self.value = value
    def __str__(self):
        return repr(self.value)