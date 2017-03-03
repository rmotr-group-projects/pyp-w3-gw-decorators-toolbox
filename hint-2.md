# Hint 2 - Timeout

The timeout decorator always causes troubles because it's "complicated" to implement. Here's an example for you to check:

```python
import signal
import time


class TimeoutError(Exception):
    pass


SECONDS_TO_WAIT = 2


def _handle_timeout(signum, frame):
    raise TimeoutError("Ahh, you took too long")

signal.signal(signal.SIGALRM, _handle_timeout)
signal.alarm(SECONDS_TO_WAIT)


def long_running_function():
    time.sleep(3)

try:
    result = long_running_function()
finally:
    signal.alarm(0)
```
