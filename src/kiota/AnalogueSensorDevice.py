import machine
from kiota.Device import Device

class AnalogueSensorDevice(Device):

#  freq = 60
  gpio = 5
  gpio_ADC = 0
  
  def __init__(self, config):
    super().__init__(config)

  def configure(self, config):
    super().configure(config)
  
  def read(self):

    pin = None
    if self.gpio is not None:
      pin = machine.Pin(self.gpio, machine.Pin.OUT)
    if pin is not None:
      pin.value(True)
    payload = { 'value': str(machine.ADC(self.gpio_ADC).read()) }
    if pin is not None:
      pin.value(False)

    return payload
