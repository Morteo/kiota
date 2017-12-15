# https://github.com/micropython/micropython-lib/blob/master/machine/machine/pin.py

# sudo pip3 install RPi.GPIO

import RPi.GPIO as GPIO

class Pin:

    IN = "in"
    OUT = "out"

    def __init__(self, no, dir=IN):
        self.gpio_no = no
        print("GPIO ########## self.gpio_no, dir={}, {}".format(self.gpio_no, dir))
        GPIO.setmode(GPIO.BCM)
        #GPIO.setmode(GPIO.BOARD)

        if dir==Pin.IN:
          GPIO.setup(self.gpio_no, GPIO.IN)
          print("GPIO >>>>>>>>>>>>>>>>>>>>>>>>>>> IN")
        else:
          GPIO.setup(self.gpio_no, GPIO.OUT)
          print("GPIO <<<<<<<<<<<<<<<<<<<<<<<<<< OUT")

    def value(self, v=None):
        if v is None:
          return GPIO.input(self.gpio_no)
        GPIO.output(self.gpio_no, v)
        print("GPIO ########## GPIO.output({},{})={}".format(self.gpio_no,v,GPIO.input(self.gpio_no)))


    def deinit(self):
        GPIO.cleanup()
