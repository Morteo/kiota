import machine
import json
import time
import dht

class Device:
  
  last_push = 0
  
  def __init__(self, config):
    pass

  def connect(self, gateway, sensor_instance):
    
      self.gateway = gateway
#      self.topic_stem = gateway.client_id + '/' + type(self).__name__ + '/' + sensor_instance
      self.topic_stem = gateway.client_id + '/' + self.config["type"] + '/' + sensor_instance
      payload = { 'connected': self.topic_stem }
      self.gateway.publish(gateway.client_id, json.dumps(payload))
  
  def publish(self):
    pass

  def push(self):
    pass

  def do_message(self, topic, b_payload):
    pass
  
  def do_push(self):
                        
    if self.config["push_frequency"] is None:
      return False
    
    if self.config["push_frequency"] < 0:
      return False
    
    if time.time() > self.last_push + self.config["push_frequency"]:

      self.last_push = time.time()
      self.push()

      return True
                        
    return False
  
  def initDevice(device_config):
    device_types = { "Switch" : Switch, "Sensor" : Sensor }
    device_class = device_types[device_config["type"]]
    device = device_class(device_config)
    return device

class Sensor(Device):

  default_config = {
        "push_frequency": 60,
        "sensor": "Moisture",
        "gpio": 4,
        "gpio_ADC": 0
  }
  
  def __init__(self, config):
    Device.__init__(self, config)
    self.config = self.default_config.copy()
    self.config.update(config)

  def connect(self, gateway):
    
      super().connect(gateway, str(self.config["sensor"]) + "/" + str(self.config["gpio"]))

      self.gateway.subscribe(self.topic_stem+"/get")

  def do_message(self, topic, b_payload):

    payload = b_payload.decode()
    
    if not(topic.startswith(self.topic_stem)):
      return False

    if topic.endswith("/get"):
      self.publish()
      return True

    return False
  
  def publish(self):

    payload = {}
  
    try:
      if self.config["sensor"] ==  "DHT22":
        d = dht.DHT22(machine.Pin(self.config["gpio"]))
        d.measure()
        payload = { 'temperature': str(d.temperature()), "humidity": str(d.humidity()) }
      elif self.config["sensor"] == "Moisture": 
        vpin = machine.Pin(self.config["gpio"], machine.Pin.OUT)
        vpin.value(True)
        # time.sleep(0.01)
        payload = { 'moisture': str(machine.ADC(self.config["gpio_ADC"]).read()) }
        vpin.value(False)

      self.gateway.publish(self.topic_stem, json.dumps(payload))
    except Exception as e:
      import sys
      sys.print_exception(e)
    
  def push(self):
     self.publish()
      
class Switch(Device):

  default_config = {
        "push_frequency": -1,
        "gpio": 12,
        "state": False
  }
  
  def __init__(self, config):
    Device.__init__(self, config)
    self.config = self.default_config.copy()
    self.config.update(config)
    
    self.pin = machine.Pin(self.config["gpio"], machine.Pin.OUT)

  def connect(self, gateway):
    
      super().connect(gateway, str(self.config["gpio"]))

      self.gateway.subscribe(self.topic_stem+"/get")
      self.gateway.subscribe(self.topic_stem+"/set")

  def do_message(self, topic, b_payload):

    if not(topic.startswith(self.topic_stem)):
      return False

    payload = b_payload.decode().lower()

    if topic.endswith("/get"):

      self.publish()
                        
    elif topic.endswith("/set"):
    
      if payload in ['1', 'true', 'on']:
        new_state = True
      elif payload in ['0', 'false', 'off' ]:
        new_state = False
      elif payload == "toggle":
        new_state = not self.config["state"]
      else: 
        return False

      self.pin.value(new_state)
      self.publish()

      return True

    return False
  
  def publish(self):
    self.config["state"] = bool(self.pin.value())
    payload = { "state": self.config["state"] }
    self.gateway.publish(self.topic_stem, json.dumps(payload))

  def push(self):
    state = bool(self.pin.value())
    if self.config["state"] != state:
      self.publish()
