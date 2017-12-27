import json
from dg_mqtt.Gateway import Gateway
import dg_mqtt.Util as Util

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
  config = Util.loadConfig('config/config.json')['WiFi']
  secret = Util.loadConfig('config/__secret__/config.json')['WiFi']
  config = Util.mergeConfig(config,secret)
  #  print("WiFi config: {}".format(json.dumps(config)))
  connectWifi(config['SSID'], config['password'])

  Gateway().start()
except Exception as e:
  import sys
  sys.print_exception(e)

# Gateway received a ../Gateway/exit message from MQTT server or encountered an unanticipated excpetion

import webrepl
# first time use of webREPL set it up 
#import webrepl_setup
#webrepl.start()
#webrepl._webrepl.password("<password>")

