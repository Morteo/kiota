import machine
import dht

from kiota.Device import Device

class DHTDevice(Device):

  freq = 60
  gpio = 14
  dht_type = 22
  
  def __init__(self, config):
    super().__init__(config)
  
  def configure(self, config):
    super().configure(config)
  
  def read(self):

    d = None
    if self.dht_type == 22:
      d = dht.DHT22(machine.Pin(self.gpio))
    else:
      d = dht.DHT11(machine.Pin(self.gpio))
      
    try:
      d.measure()
      payload = { 'temperature': str(d.temperature()), "humidity": str(d.humidity()) }
      return payload
    except Exception as e:
      import kiota.Util as Util
      Util.log(self,"DHT type: {}, failed to measure pin: '{}'".format(self.dht_type, self.gpio))
      import sys
      sys.print_exception(e)
   