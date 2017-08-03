# Hint 2 - Timeout

The timeout decorator causes trouble because the easiest way to implement it is tightly related to an Operating System feature called **[_signals_](http://www.thegeekstuff.com/2012/03/linux-signals-fundamentals/)**. We don't need to do a masters on signals to implement the `timeout` decorator. The only thing you need to know is about the [signals Python implementation](https://docs.python.org/2/library/signal.html), and the [alarm function](https://docs.python.org/2/library/signal.html#signal.alarm).

Think about your day to day, morning alarm. The one that wakes you up in the morning (we love it, right?)

A Python _alarm_ is the same concept as our regular phone alarm, but applied to our code. With an alarm, we can set a special type of signal in order to get _notified_ by the operating system of a given event. For example, when a given number of seconds pass (Sounds familiar?). Check the following example (borrowed from [pymotw](https://pymotw.com/2/signal/#alarms)):

```python
import signal
import time

def receive_alarm(signum, stack):
    print('Alarm :', time.ctime())

# Call receive_alarm in 2 seconds
signal.signal(signal.SIGALRM, receive_alarm)
signal.alarm(2)

print('Before:', time.ctime())
time.sleep(4)  # long running task ;)
print('After :', time.ctime())
```
