
import machine

from dg_mqtt.Device import Device
import dg_mqtt.Util as Util


class SwitchDevice(Device):

  default_config = {
    "poll_frequency": None,
    "publish_changes_only": False,
    "gpio": 12,
    "state": False
  }
  
  def __init__(self, config):
    super().__init__(config)
  
  def configure(self, config):
    super().configure(config)
    self.pin = machine.Pin(self.config["gpio"], machine.Pin.OUT)
    
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
    
#    Util.log(self,"write final state '{}' payload: '{}'  pin 15 state: '{}'".format(self.pin.value(), payload,machine.Pin(15, machine.Pin.OUT).value()))

    return self.read()
