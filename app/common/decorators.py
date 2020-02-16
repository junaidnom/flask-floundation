from functools import wraps


def with_thread(func):
    from threading import Thread
    from functools import wraps

    @wraps(func)
    def threaded_func(*args, **kwargs):
        job = Thread(target=func, args=args, kwargs=kwargs)
        job.start()
        return job

    return threaded_func
