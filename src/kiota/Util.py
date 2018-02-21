
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
    
    
def mergeConfig(base, update):
    
    if update is None:
        return base 
      
    for key in base:

      try:
        update_value = update[key]
      except (KeyError):
        None
      else:
        if update_value is not None:
          
          base_value = base[key]
          if isinstance(base_value, dict) and isinstance(update_value, dict):
            base[key] = mergeConfig(base_value, update_value)
          else:
            base[key] = update_value
                    
    for key in update:
      
      if key not in base:
          base[key] = update[key]
          
    return base;
                   
  
  
  
  
  
  
  
  
  
  
  
  

