#!/usr/bin/python3

import machine

config = {
  "gateway": {
#    "type": "electrodragon-wifi-iot-relay-board-spdt-based-esp8266"
    "id": "power_strip"
#    "description": "Portable WiFi Power strip "
  },
  "devices": [
    {
      "type": "SwitchDevice",
      "id": "left_socket", 
#      "description": "Relay corner out controls central heating on/off",
      "gpio": 13,
      "state": False
    },    
    {
      "type": "SwitchDevice",
      "id": "right_socket", 
#      "description": "Relay corner out controls central heating on/off",
      "gpio": 12,
      "state": False
    }    
  ]
}
