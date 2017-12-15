from .exceptions import FunctionTimeoutException

'''
python
import signal
import time

# Call receive_alarm in 2 seconds
signal.signal(signal.SIGALRM, receive_alarm)
signal.alarm(2)

print('Before:', time.ctime())
time.sleep(4)  # long running task ;)
print('After :', time.ctime())
'''

#Useful to given functions a certain max time for execution. The decorator is suppose to track the 
#execution time and raise and exception if the time exceeds given timeout range. Example:
import signal
import time

# class MyVeryCoolException(Exception):
#   pass
# what is the timming between alarm and time out
# Class exception import error


#raise FunctionTimeoutException -- where should I raise the exception

def timeout(max_time , exception = FunctionTimeoutException): 
    def receive_alarm(signum, stack):
        raise exception('Function call timed out')
        print('Alarm :', time.ctime())

    def wrapper(func):
        def func_wrapper(*args, **kwargs):
            #write your code here
            print(max_time)
            signal.signal(signal.SIGALRM, receive_alarm) # alarm will raise after max_time, first line is listening to second line
            signal.alarm(max_time)
            t1 = time.time()
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            t2 = time.time() - t1
            print('{} rans for {} secs'.format(func.__name__, t2))
            return result     
        return func_wrapper
    return wrapper    
    
@timeout(5,FunctionTimeoutException)
def very_slow_function():
    time.sleep(1)
    print('I am here')
    

very_slow_function()
#time.sleep(10)


