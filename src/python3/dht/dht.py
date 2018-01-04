
# see https://github.com/micropython/micropython/blob/master/esp8266/modules/dht.py 

import Adafruit_DHT

class DHTBase:
    def __init__(self, sensor, pin):
      self.sensor = sensor
      self.pin = pin

    def measure(self):
      self.humidity, self.temperature = Adafruit_DHT.read_retry(self.sensor, self.pin.gpio_no)

    def humidity(self):
      return self.humidity

    def temperature(self):
      return self.temperature

class DHT11(DHTBase):

    def __init__(self, pin):
      super().__init__(Adafruit_DHT.DHT11, pin)

class DHT22(DHTBase):
  
    def __init__(self, pin):
      super().__init__(Adafruit_DHT.DHT22, pin)
