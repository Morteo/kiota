import machine
import json

from kiota.Device import Device

class TransmitterDevice(Device):

  gpio = 15
#  retries = 10
#  start_value = False
#  pattern = 10000, 10000, 300, 700, 700, 700, 300
  
  def __init__(self, config):
    super().__init__(config)
  
  def configure(self, config):
    super().configure(config)
    self.pin = machine.Pin(self.gpio, machine.Pin.OUT)
#    self.pin = machine.Pin(self.gpio, machine.Pin.OPEN_DRAIN)

  def write(self, payload):
    
    start_value = self.start_value
    pattern = self.pattern
    
    if payload is not None:
      p = None
      try:
        import ujson as json
        p = json.loads(payload)
      except (OSError, ValueError):
        import kiota.Util as Util
        Util.log(self,"Can parse payload: '{}'".format(payload))
      else:
        try: start_value = p["start_value"] 
        except (KeyError): pass
        try: pattern = p["pattern"] 
        except (KeyError): pass

    return { "transmission": bool(TransmitterDevice.transmit(self.pin,  self.retries, start_value, pattern)) }

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
