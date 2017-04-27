import machine
import dht
from dg_mqtt.Device import Device

class DHT22Device(Device):

  default_config = {
        "poll_frequency": 60,
        "publish_changes_only": False,
        "gpio": 14
  }
  
  def __init__(self, config):
    super().__init__(config)
  
  def configure(self, config):
    super().configure(config)
  
  def read(self):

    d = dht.DHT22(machine.Pin(self.config["gpio"]))
    d.measure()
    payload = { 'temperature': str(d.temperature()), "humidity": str(d.humidity()) }

    return payload
