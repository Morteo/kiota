from dg_mqtt.gateway import Gateway
from dg_mqtt.Util import ConfigFile

try:
  config = ConfigFile('dg_mqtt/config.json').config
  Gateway(config).start()
except Exception as e:
  import sys
  sys.print_exception(e)

# Gateway received a ../Gateway/exit message from MQTT server or encountered an unanticipated excpetion

import webrepl
webrepl.start()
