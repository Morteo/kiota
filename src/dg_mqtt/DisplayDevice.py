       
import machine
import json
import utime

from dg_mqtt.Device import Device

############################################
############################################
# Skeleton Outline - Only !!!!!!!!!!!!!!!!
############################################
############################################


class DisplayDevice(Device):

  default_config = {
          "poll_frequency": None,
          "publish_changes_only": False,
    
          "width": 128,
          "height": 64,
    
          "display_type": "SSD1306_I2C",
    
          "I2C": {
            "bitbanging_mode": True, # Use software implementation?
            "id": -1, # use -1 for bitbanging
            "freq": 800000,
#            "gpio_res": 0 # Reset
            "gpio_scl": 4, # clock, not used for non-bitbanging hardware implementatino 
            "gpio_sda": 5 # data, not used for non-bitbanging hardware implementatino 
          },
          "SPI": {
            "bitbanging_mode": False, # Use software implementation?
            "id": 1, # use -1 for bitbanging
            "baudrate": 1000000,
            "polarity": 0, # the idle state of SCK,  For bitbanging use 1
            "phase": 0, # 0 is sample on the first edge of serial clock and 1 for the second
            "gpio_sck": 14, # Serial Clock, not used for non-bitbanging hardware implementatino 
            "gpio_mosi": 13, # Master Output, Slave Input, not used for non-bitbanging hardware implementatino 
            "gpio_miso": 12, # Master Input, Slave Output, not used for non-bitbanging hardware implementatino 
            "gpio_dc": 12,  # Data / Command. Same as MISO
            "gpio_res": 5, # Reset
            "gpio_cs": 15 # Chip Select
          }
  }
  
  def __init__(self, config):
    super().__init__(config)
  
  def configure(self, config):
    super().configure(config)

    self.display = None
    
    if self.config["display_type"] == "SSD1306_I2C":
      
      i2c = None

      if self.config["I2C"]["bitbanging_mode"]:
        
        i2c = machine.I2C(-1,
                  freq=self.config["I2C"]["freq"], 
                  scl=machine.Pin(self.config["I2C"]["gpio_scl"],
                  sda=machine.Pin(self.config["I2C"]["gpio_sda"])

      else:
      
        i2c = machine.I2C(self.config["SPI"]["id"], 
                  freq=self.config["I2C"]["freq"])
      
      import ssd1306

      self.display = ssd1306.SSD1306_I2C(
                  self.config["width"], 
                  self.config["height"], 
                  i2c)
                                   
      
    elif self.config["display_type"] == "SSD1306_SPI":

      spi = None
      
      if self.config["SPI"]["bitbanging_mode"]:
        
        spi = machine.SPI(self.config["SPI"]["id"], 
                  baudrate=self.config["SPI"]["baudrate"], 
                  polarity=self.config["SPI"]["polarity"], 
                  phase=self.config["SPI"]["phase"],
                  sck=machine.Pin(self.config["SPI"]["gpio_sck"],
                  mosi=machine.Pin(self.config["SPI"]["gpio_mosi"],
                  miso=machine.Pin(self.config["SPI"]["gpio_miso"])
        
      else:
      
        spi = machine.SPI(self.config["SPI"]["id"], 
                  baudrate=self.config["SPI"]["baudrate"], 
                  polarity=self.config["SPI"]["polarity"], 
                  phase=self.config["SPI"]["phase"])
      
      import ssd1306

      self.display = ssd1306.SSD1306_SPI(
                  self.config["width"], 
                  self.config["height"], 
                  spi,
                  machine.Pin(self.config["SPI"]["gpio_dc"],
                  machine.Pin(self.config["SPI"]["gpio_res"],
                  machine.Pin(self.config["SPI"]["gpio_cs"])
                              
  def write(self, payload):
    return { "display": bool(DisplayDevice.display_exec(self.display, payload)) }

  def display_exec(display, command):

# display.fill(0)
# display.pixel(0, 0, 1)
# display.text('Hello', 0, 0)
# display.text('World', 10, 20)
# display.show()
# display.invert(True)
# display.invert(False)

      loc = { "display": display }
      exec(command, globals(), loc)

    return True     
