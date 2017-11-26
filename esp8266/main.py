from dg_mqtt.gateway import Gateway


def do_connect():
    import network

    SSID = 'MORTEO_NET'
    PASSWORD = 'M0rt30_n3t'

    sta_if = network.WLAN(network.STA_IF)
    ap_if = network.WLAN(network.AP_IF)
    if ap_if.active():
        ap_if.active(False)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(SSID, PASSWORD)
        while not sta_if.isconnected():
            pass
    print('Network configuration:', sta_if.ifconfig())


do_connect()

try:
  gateway = Gateway('config.json')
except Exception as e:
  import sys
  sys.print_exception(e)

# Gateway received a ../Gateway/exit message from MQTT server or encountered an unanticipated excpetion

import webrepl
webrepl.start()

