import machine
from kiota.Device import Device

class SwitchDevice(Device):

  switch_type = machine.Pin.OUT
  gpio = 12
  state = None

## Example as TriggerDevice
#  switch_type = machine.Pin.IN      
#  gpio = 4
#  freq = 0
#  just_changes = True
#   
  
  def __init__(self, config):
    super().__init__(config)
  
  def configure(self, config):
    super().configure(config)
    self.pin = machine.Pin(self.gpio, self.switch_type)
    if self.state is not None:
      self.pin.value(bool(self.state))
  
  def read(self):
    
    payload = { "state": bool(self.pin.value()) }
#    import kiota.Util as Util
#    Util.log(self,"read state payload: '{}' from pin: '{}'".format( payload,self.gpio))
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
#      return { "error": "Unsupported state: {}".format(payload) }
      return { "error": payload }

    self.pin.value(new_state)
    
#     import kiota.Util as Util
#     Util.log(self,"write final state '{}' payload: '{}'  pin 15 state: '{}'".format(self.pin.value(), payload,machine.Pin(15, machine.Pin.OUT).value()))

    return self.read()
