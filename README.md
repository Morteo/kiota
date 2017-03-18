# KIOT Karl's Internet of Things kiot

## esp8266 dg_mqtt
MQTT Device Gateway -  MircoPython code for ElectroDragon ESP Relay Board.

* ElectroDragon flashed with MicroPython firmware (esp8266-20160909-v1.8.4.bin) 
* Connecting to Mosquitto MQTT server (1.4.9) 

### Installation 
* Add WiFI credentials to boot.py
* Add MQTT server configuration to config.json
* Add configuration for each device connected to esp8266 to config.json

#### Gateway 

Configuration

  "Gateway": {  
    "server": "192.168.1.99",
    "username": "*secret*",
    "password": "*secret*"
  },
  "Devices": [
  ]
  ),

Subscribes to

    topic = "/devices/[MAC ADDR]/esp8266/Gateway/exit"
    payload ignored
    action = shutdown gateway and exit to WebREPL

#### Devices 

Configuration

    "type":  "Switch" | "Sensor", 
    "description": "short text",
    "push_frequency": -1, // frequency in seconds that status is published.Use  -1 for status push

On instantiation publishes

    topic = "/devices/[MAC ADDR]/esp8266"
    payload = { 'connected': '/devices/[MAC ADDR]/esp8266/[DEVICE TYPE]/[DEVICE INFO]' }


**Switch Device**

Used for the 2 ElectroDragon relays on PIN 12 and 13.

Configuration

    "type": "Switch", 
    "gpio": 12,
    "state": false, // The state to initialze the GPIO 

Subscribes to

    topic = "/devices/[MAC ADDR]/esp8266/Switch/[GPIO]/get"
    action = publish GPIO state on topic "/devices/[MAC ADDR]/esp8266/Switch/[GPIO]"

    topic = "/devices/[MAC ADDR]/esp8266/Switch/[GPIO]/set"
    payload in ['1', 'true', 'on', '0', 'false', 'off', 'toggle']
    action = changes the GPIO state publishes new state
 
**DHT22 Sensor Device** - Tempurature and Humidty

Used for the ElectroDragon DHT connection PIN 14

Configuration

    "type": "Sensor", 
    "sensor": "DHT22",
    "gpio": 14,  

Subscribes to

    topic = "/devices/[MAC ADDR]/esp8266/Sensor/DHT22/[GPIO]/get"
    action = publish sensor value
    payload = { 'temperature': [99], "humidity":  [99] }

**Moisture Sensor Device** - Soil Hygrometer 

Configuration

    "type": "Sensor", 
    "sensor": "Moisture",
    "gpio": 5,
    "gpio_ADC": 0

Subscribes to

    topic = "/devices/[MAC ADDR]/esp8266/Sensor/Moisture/[GPIO]/get"
    action = publish sensor value
    payload = { 'moisture': [99] }

