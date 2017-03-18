
class Log:

  DEBUG = True
  
  def log(o, t, e=None):
#    if self.DEBUG:
      if e is None:
        print("{}: {}".format(type(o).__name__, t))
      else:
        print("{}: {} Exception:{!r}".format(type(o).__name__, t, e))
        import sys
        sys.print_exception(e)

class ConfigFile:

  filepath = None
  config = {}
  
  def __init__(self, filepath=None):
    
    self.filepath = filepath
    if filepath is not None:
      self.load(filepath)
      
  def load(self,filepath):
    import ujson as json
    try:
      with open(filepath) as f:
        self.config.update(json.loads(f.read()))
        self.filepath = filepath
    except (OSError, ValueError):
      print('{}: failed to load from file: {}'.format(type(self).__name__, filepath))
    else:
      print('{}: loaded from file: {}'.format(type(self).__name__, filepath))
      return self.config

  def saveAs(self,filepath=None):
    import ujson as json

    if filepath is None:
      filepath = self.filepath
    
    try:
      with open(filepath, "w") as f:
        f.write(json.dumps(self.config))
        self.filepath = filepath
    except OSError:
      print('{}: failed to save to file: {}'.format(type(self).__name__, filepath))
    else:
      print('{}: saved to file: {}'.format(type(self).__name__, filepath))
      return True
