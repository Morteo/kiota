
def log(o, t, e=None):
  if e is None:
    print("{}: {}".format(type(o).__name__, t))
  else:
    print("{}: {} Exception:{!r}".format(type(o).__name__, t, e))
    import sys
    if hasattr(sys, 'print_exception'):
      sys.print_exception(e)
    else:
      import traceback
      traceback.print_exception(type(e), e, sys.exc_info()[2])
