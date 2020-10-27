from .logger import logger
import traceback
import threading
import sys

def run_on_thread(func, args, kwargs, daemon=True):
    def run():
        thread.ret = None
        try:
            thread.ret = func(*args, **kwargs)
        except Exception:
            logger.exception(
                "thread exception %s", traceback.print_exception(*sys.exc_info()))

    def get_ret(timeout=2.0):
        try:
            thread.join(timeout)
        except Exception:
            logger.exception(
                "thread exception %s", traceback.print_exception(*sys.exc_info()))
        finally:
            if thread.is_alive():
                logger.error("%s, thread unfinished, join failed", func.__name__)
        return thread.ret

    thread = threading.Thread(None, run)
    thread.exc = None
    thread.get_ret = get_ret
    thread.setDaemon(daemon)
    thread.start()
    return thread