from . import _ext

def add(a, b):
    return _ext.add(a, b)

add.__doc__ = _ext.add.__doc__
