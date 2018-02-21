from kiota.Gateway import Gateway
#import kiota.Util as Util

def connectWifi(SSID, password):
  
    import network
    
    sta_if = network.WLAN(network.STA_IF)
    ap_if = network.WLAN(network.AP_IF)
    if ap_if.active():
        ap_if.active(False)
    if not sta_if.isconnected():
        print("connecting to network...")
        sta_if.active(True)
        sta_if.connect(SSID, password)
        while not sta_if.isconnected():
            pass
    print("Network configuration: {}".format(sta_if.ifconfig()))

try:
  from kiota.Configurator import Configurator
  config = Configurator.load()
#  print(config)
  connectWifi(config["wifi"]["SSID"], config["wifi"]["password"])
  Gateway(config).start()
  
except Exception as e:
  import sys
  sys.print_exception(e)

# Gateway received a ../exit message from MQTT server or encountered an unanticipated excpetion

#import webrepl
# first time use of webREPL set it up 
#import webrepl_setup
#webrepl.start()
#webrepl._webrepl.password("<password>")
