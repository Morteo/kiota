       
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
#    self.pin = machine.Pin(self.config["gpio"], machine.Pin.OPEN_DRAIN)

  def write(self, payload):
    config = self.config.copy()
    config.update(json.loads(payload))
    return { "transmission": bool(TransmitterDevice.transmit(self.pin,  config["retries"], config["start_value"], config["pattern"])) }

  def transmit(pin, retries, start_value, pattern):
#    print("pin: {} retries: {} start_value: {} pattern: {}".format(pin, retries, start_value, pattern))
    state = pin.value
    sleep = utime.sleep_us
    
    for a in range(retries):
      value = start_value
      for i in range(len(pattern)):
        state(value)
        sleep(pattern[i])
        value = not(value)
        
    return True     
