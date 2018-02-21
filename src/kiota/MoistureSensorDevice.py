import machine
from dg_mqtt.Device import Device

class MoistureSensorDevice(Device):

  default_config = {
        "poll_frequency": 60,
        "publish_changes_only": False,
        "gpio": 5,
        "gpio_ADC": 0
  }
  
  def __init__(self, config):
    super().__init__(config)

  def configure(self, config):
    super().configure(config)
    self.pin = machine.Pin(self.config["gpio"], machine.Pin.OUT)
  
  def read(self):

    self.pin.value(True)
    payload = { 'moisture': str(machine.ADC(self.config["gpio_ADC"]).read()) }
    self.pin.value(False)

    return payload
