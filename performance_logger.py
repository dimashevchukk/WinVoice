import time
from functools import wraps

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time() - start
        print(f'{func.__name__} took {end:.2f} sec.')
        return result
    return wrapper
