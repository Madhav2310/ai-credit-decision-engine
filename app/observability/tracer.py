def trace(name):
    def wrapper(func):
        def inner(*args, **kwargs):
            return func(*args, **kwargs)
        return inner
    return wrapper