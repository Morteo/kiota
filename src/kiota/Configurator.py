
class Configurator():
  def load():
    import config

    try:
      import __secrets__
      Configurator.apply(config.config, __secrets__.config)
    except ImportError:
      pass

    return config.config

  def apply(base, config):
#      print("base={}".format(base))
#      print("config={}".format(config))
      if isinstance(config, dict):
        for key, value in config.items():
          if not key.startswith('__'): # and not callable(value):
            if isinstance(base, dict):
              if isinstance(value, dict) and key in base and base[key] is not None:
                Configurator.apply(base[key], value)
              else:
#                print("base[{}]={}".format(key, value))
                base[key] = value
            else:
              if isinstance(value, dict) and hasattr(base, key) and getattr(base, key) is not None:
                Configurator.apply(getattr(base, key), value)
              else:
#                print("base.{}={}".format(key, value))
                setattr(base, key, value)
