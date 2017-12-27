import sys
import time
import json

import machine
from umqtt.simple import MQTTClient

try:
  import ubinascii
except ImportError:
  import binascii as ubinascii 

try:
  import uhashlib
except ImportError:
  import hashlib as uhashlib
 
from dg_mqtt.Device import Device
import dg_mqtt.Util as Util

class ExitGatewayException(Exception):
    pass

class Gateway:
 
  default_config = {
    "Gateway": {  
      'MQTTServer': {
        'server': "192.168.1.123",
        'port': 1883,
        'keep_alive': 60,
        'username': "********",
        'password': "********",
        'wait_to_reconnect': 5
      }
    }
  }
  
  last_ping = 0

  def __init__(self, start=True):

    config = Util.loadConfig('config/config.json')
    secret = Util.loadConfig('config/__secret__/config.json')
    config = Util.mergeConfig(config, secret)
    
    self.config =  Util.mergeConfig(self.default_config.copy(), config['Gateway'])
    
    self.configure(config)

    if start:
      self.start()
    
  def configure(self, config):

    self.devices = []

    if self.config['id'] is None:
        self.config['id'] = ubinascii.hexlify(uhashlib.sha256(machine.unique_id()).digest()).decode()

#    if self.config['version'] is None:
#        import network
#        self.topic = "/devices/" +ubinascii.hexlify(network.WLAN().config('mac')).decode() + "/esp8266"
#    else:
    self.topic = "/devices/" + self.config['id']

    self.client = MQTTClient(self.topic, 
                             self.config['MQTTServer']['server'], 
                             self.config['MQTTServer']['port'], 
                             self.config['MQTTServer']['username'], 
                             self.config['MQTTServer']['password'], 
                             self.config['MQTTServer']['keep_alive'])
    self.client.set_callback(self.do_message_callback)
    self.exit_topic = self.topic+"/gateway/exit"
    
    for device_config in config["Devices"]:

      device_config.setdefault("module", None)
      device_config.setdefault("id", None)
      device_config.setdefault("description", None)
      
      try:
        
        class_name =  device_config["type"]
        print(class_name)

        module_name = "dg_mqtt"
        if device_config["module"] is not None:
          module_name = device_config["module"]
        print(module_name)

        module = __import__(module_name, class_name)
        #module = sys.import_module(module_name)
        print(module)
        
        klass = getattr(module, class_name)
        #klass = module[class_name]
        print(klass)
    
        device = klass(device_config)
        self.devices.append(device) 
        
      except ImportError as e:
        Util.log(self,"error: '{}' config: '{}'".format(e,device_config))


  def connect(self):
    self.client.connect()
    Util.log(self,"connect to MQTT server on {}:{} as {}".format(
        self.config['MQTTServer']['server'], 
        self.config['MQTTServer']['port'], 
        self.config['MQTTServer']['username']))
    self.subscribe(self.exit_topic)
    for device in self.devices: 
      device.connect(self)

  def subscribe(self, topic):
    self.client.subscribe(topic.encode())
        
  def publish(self, topic, payload):
    Util.log(self,"sent: topic '{}' payload: '{}'".format(topic,payload))
    self.client.publish(topic.encode('utf-8'), payload)
    
  def start(self):

    while True:
      try:
        self.connect()
        while True:
          #time.sleep(0.01) # attempt to reduce number of OSError: [Errno 104] ECONNRESET 
          self.client.check_msg()
          #time.sleep(0.01) # attempt to reduce number of OSError: [Errno 104] ECONNRESET 
          self.push()
          time.sleep(0.01)
      except OSError as e:
          Util.log(self,"failed to connect, retrying....", e)
          time.sleep(self.config['MQTTServer']["wait_to_reconnect"])

    self.client.disconnect()
    
  def push(self):
    if time.time() > self.last_ping + self.config['MQTTServer']["keep_alive"]/3:
      self.last_ping = time.time()
      self.client.ping()
    for device in self.devices: 
      device.push()
      
  def do_message_callback(self, b_topic, payload):
    topic = b_topic.decode() #convert to string
    Util.log(self,"received: topic '{}' payload: '{}'".format(topic,payload))
    if topic == self.exit_topic:
      raise ExitGatewayException()
    for device in self.devices: 
      if device.do_message(topic, payload):
#        Util.log(self,"consumed: topic '{}' payload: '{}' by device {}".format(topic,payload,json.dumps(device.config)))
        break
        