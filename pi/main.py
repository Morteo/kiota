#!/usr/bin/python3
import json
from dg_mqtt.Gateway import Gateway
from dg_mqtt.Util import ConfigFile

try:
  config = ConfigFile('config/config.json').config
  print("config: {}".format(json.dumps(config)))
  config.update(ConfigFile('config/__secret__/config.json').config)

  Gateway(config).start()
except Exception as e:
  import sys
  import traceback
  traceback.print_exception(None, e, sys.exc_info()[2])
