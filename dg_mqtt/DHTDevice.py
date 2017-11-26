import machine
import dht

from dg_mqtt.Device import Device
import dg_mqtt.Util as Util

class DHTDevice(Device):

  default_config = {
        "poll_frequency": 60,
        "publish_changes_only": False,
        "gpio": 14,
        "dht_type": 22
  }
  
  def __init__(self, config):
    super().__init__(config)
  
  def configure(self, config):
    super().configure(config)
  
  def read(self):

    d = None
    if self.config['dht_type'] == 11:
      d = dht.DHT22(machine.Pin(self.config["gpio"]))
    else:
      d = dht.DHT11(machine.Pin(self.config["gpio"]))
      
    try:
      d.measure()
      payload = { 'temperature': str(d.temperature()), "humidity": str(d.humidity()) }
      return payload
    except Exception as e:
      Util.log(self,"DHT type: {}, failed to measure pin: '{}'".format(self.config["dht_type"], self.config["gpio"]))
      import sys
      sys.print_exception(e)
   