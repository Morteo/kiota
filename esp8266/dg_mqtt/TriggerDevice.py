import machine
from dg_mqtt.Device import Device

class TriggerDevice(Device):

  default_config = {
        "poll_frequency": 1,
        "publish_changes_only": True,
        "gpio": 4,
        "state": None
  }
  
  def __init__(self, config):
    super().__init__(config)
  
  def configure(self, config):
    super().configure(config)
    self.pin = machine.Pin(self.config["gpio"], machine.Pin.OPEN_DRAIN)
    
    if self.config['state'] is not None:
      self.pin.value(bool(self.config['state']))
  
  def read(self):
    payload = { "state": bool(self.pin.value()) }
    return payload
    
  def write(self, payload):
    
    new_state = None
    
    if payload in ['1', 'true', 'on']:
      new_state = True
    elif payload in ['0', 'false', 'off' ]:
      new_state = False
    elif payload == "toggle":
      new_state = not bool(self.pin.value())
    else: 
      return { "error": "Unsupported state: {}".format(payload) }
        
    self.pin.value(new_state)
    return self.read()
