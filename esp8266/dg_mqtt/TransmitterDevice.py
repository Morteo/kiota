import machine
import json
import utime
from dg_mqtt.Device import Device

class TransmitterDevice(Device):

  default_config = {
          "poll_frequency": None,
          "publish_changes_only": False,
          "gpio": 15,
          "retries": 10,
          "start_value": False,
          "pattern": [ 10000, 10000, 300, 700, 700, 700, 300]
  }
  
  def __init__(self, config):
    super().__init__(config)
  
  def configure(self, config):
    super().configure(config)
    self.pin = machine.Pin(self.config["gpio"], machine.Pin.OUT)

  def write(self, payload):
    config = self.config.copy()
    config.update(json.loads(payload))
    return { "transmission": transmit(self.pin,  config.payload["retries"], config.payload["start_value"], config.payload["pattern"]) }

  def transmit(pin, retries, start_value, pattern):
    state = pin.value
    sleep = utime.sleep_us
    value = start_value
    
    for a in range(retries):
      for i in range(len(pattern)):
        state(value)
        sleep(pattern[i])
        value = not(value)
        
    return True     
