#! /usr/bin/env python 2.7

import logging
import threading

def async_function(func):
    def func_wrapper(*args, **kwargs):
        try:
            th = threading.Thread(target=func, args=args, kwargs=kwargs)
            th.setDaemon(True)
            th.start()
            th.join()
            return True
        except Exception, e:
            logging.exception(e)
            return False
    return func_wrapper
