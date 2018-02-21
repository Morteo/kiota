import machine

from kiota.Device import Device

class DisplayDevice(Device):

  width = 128
  height = 64
  display_type = "SSD1306_I2C"
  
  class I2C:
    bus = -1        # -1 tells it to use bitbanging.
    gpio_scl = 4    # clock, not used for non-bitbanging hardware implementatino 
    gpio_sda = 5    # data, not used for non-bitbanging hardware implementatino 
    # not supported, uses default.
    # sda = 0x3c  #  device_addr - display I2C address
    # not supported, uses default.
    # max_freq = 25000, #slow
    # not required to know which pin
    # gpio_res = 0 # Reset.
    
  class SPI:
    id = 1                    # use -1 for bitbanging
#    bitbanging_mode = False   # Use software implementation?
#    baudrate = 1000000
#    polarity = 0              # the idle state of SCK,  For bitbanging use 1
#    phase = 0                 # 0 is sample on the first edge of serial clock and 1 for the second
#    gpio_sck = 14             # Serial Clock, not used for non-bitbanging hardware implementatino 
#    gpio_mosi = 13            # Master Output, Slave Input, not used for non-bitbanging hardware implementatino 
#    gpio_miso = 12            # Master Input, Slave Output, not used for non-bitbanging hardware implementatino 
#    gpio_dc = 12              # Data / Command. Same as MISO
#    gpio_res = 5              # Reset
#    gpio_cs = 15              # Chip Select

  i2c = I2C()
  spi = SPI()
  
  def __init__(self, config):
    
    self.update_display_function = DisplayDevice.update_display
    
    super().__init__(config)
  
  def configure(self, config):
    
    super().configure(config)

    import ssd1306

    self.display = None

    try:
      
      if self.display_type == "SSD1306_I2C":

          i2c = machine.I2C(
                    self.i2c.bus,
                    scl=machine.Pin(self.i2c.gpio_scl),
                    sda=machine.Pin(self.i2c.gpio_sda)
#                    freq=self.i2c.max_freq
          )

#          addrs = i2c.scan()
#          print("Scanning I2C devices:", [hex(x) for x in addrs])
#          if self.sla not in addrs:
#            import ubinascii
#            print("ICT device not detected on address", ubinascii.hexlify(device_addr))

          self.display = ssd1306.SSD1306_I2C(
                    self.width, 
                    self.height, 
                    i2c
          )

          self.display.poweron()

      elif self.display_type == "SSD1306_SPI":

        spi = None

        if self.bitbanging_mode:

          spi = machine.SPI(self.spi.id, 
                    baudrate=self.spi.baudrate,
                    polarity=self.spi.polarity, 
                    phase=self.spi.phase,
                    sck=machine.Pin(self.spi.gpio_sck),
                    mosi=machine.Pin(self.spi.gpio_mosi),
                    miso=machine.Pin(self.spi.gpio_miso))

        else:

          spi = machine.SPI(self.spi.id, 
                    baudrate=self.spi.baudrate, 
                    polarity=self.spi.polarity, 
                    phase=self.spi.phase)

        self.display = ssd1306.SSD1306_SPI(
                    self.width, 
                    self.height, 
                    spi,
                    machine.Pin(self.spi.gpio_dc),
                    machine.Pin(self.spi.gpio_res),
                    machine.Pin(self.spi.gpio_cs))

    except OSError as e:
      import kiota.Util as Util
      Util.log(self,"failed to configure display", e)
                              
  def write(self, payload):
    
    ok = False
    
    try:
      ok = bool(self.update_display_function(self.display, payload))
    except Exception as e:
      import kiota.Util as Util
      Util.log(self,"failed to update display", e)
      
    return { "display": ok }

  def update_display(display, command):

    display.fill(0)
    display.text(command, 0, 0)
    display.show()

    return True
