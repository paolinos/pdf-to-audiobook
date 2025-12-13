from typing import Callable


def no_print(*args):
    pass


class Logger:
    """
    Logger similar to real logging, but we're using cli so we do some simple print
    """

    _isdebug: bool

    _debugfn: Callable

    def __init__(self, debug: bool = False):
        self._isdebug = debug

        if self._isdebug is False:
            # disable debug
            self._debugfn = no_print
        else:
            self._debugfn = print

    def debug(self, *args):
        self._debugfn("[DEBUG] ", *args)

    def info(self, *args):
        print(*args)
