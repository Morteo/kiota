#!/usr/bin/python3

import machine
from update_display import update_display as update_display_function

config = {
  "gateway": {
#    "type": "electrodragon-wifi-iot-relay-board-spdt-based-esp8266"
    "id": "thermostat"
#    "description": "Thermostat Control near Kitchen"
  },
  "devices": [
    {
      "type": "DisplayDevice",
      "id": "display", 
#      "description": "OLED IC2 128 x 64 display",
      "update_display_function": update_display_function,
      "width": 128,
      "height": 64,
      "display_type": "SSD1306_I2C",
      "i2c": {
        "bus": -1,
        "gpio_scl": 4,
        "gpio_sda": 5
      }
    },
    {
      "type": "DHTDevice",
      "id": "dht", 
#      "description": "Digital Humidity and Temperature sensor",
      "dht_type": 22,
      "gpio": 14,
      "just_changes": True,
      "freq": 60
    },
    {
      "type": "SwitchDevice",
      "id": "heating_relay", 
#      "description": "Relay corner out controls central heating on/off",
      "gpio": 13,
      "state": False
    },
    {
      "type": "SwitchDevice",
      "id": "red_button", 
#      "description": "Physical impulse switch",
      "switch_type": machine.Pin.IN,      
      "gpio": 15,
#      "gpio": 2,
      "freq": 0,
      "debounce": 20,
      "just_changes": True,
      "state": False
    }    
  ]
}
