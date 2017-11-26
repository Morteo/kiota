
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
          
import json

def loadConfig(filepath):
  config = {}
  try:
    with open(filepath) as f:
      config.update(json.loads(f.read()))
  except (OSError, ValueError):
    print('loadConfig: failed to load from file: {}'.format(filepath))
  else:
    print('loadConfig: loaded from file: {}'.format(filepath))
    return config

def saveConfig(config, filepath):

  try:
    with open(filepath, "w") as f:
      f.write(json.dumps(config))
  except OSError:
    print('saveConfig: failed to save to file: {}'.format(filepath))
  else:
    print('saveConfig: saved to file: {}'.format(filepath))
