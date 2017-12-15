import json
from dg_mqtt.Gateway import Gateway
from dg_mqtt.Util import ConfigFile

def connectWifi(SSID, password):
    import network

    sta_if = network.WLAN(network.STA_IF)
    ap_if = network.WLAN(network.AP_IF)
    if ap_if.active():
        ap_if.active(False)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(SSID, password)
        while not sta_if.isconnected():
            pass
    print('Network configuration:', sta_if.ifconfig())


try:
  config = ConfigFile('config/config.json').config
  print("config: {}".format(json.dumps(config)))
  config.update(ConfigFile('config/__secret__/config.json').config)
  connectWifi(config['WiFi']['SSID'], config['WiFi']['password'])
  
  Gateway(config).start()
except Exception as e:
  import sys
  sys.print_exception(e)

# Gateway received a ../Gateway/exit message from MQTT server or encountered an unanticipated excpetion

import webrepl
webrepl.start()

