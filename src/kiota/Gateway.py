import sys
import time
import json

import machine
from umqtt.simple import MQTTClient

from kiota.Device import Device
import kiota.Util as Util

class ExitGatewayException(Exception):
    pass

class Gateway:
 
  id = None
#  description = None
#  gateway_type = None

  class MQTTServer:
#    server = "192.168.1.123"
#    port = 1883
#    keep_alive = 60
#    username = "*"
#    password = "*"
    wait_to_reconnect = 5

  mqtt_server = MQTTServer()
    
  def __init__(self, config, start=True):

    self.configure(config)

    if start:
      self.start()
    
  def configure(self, config):
    
    from kiota.Configurator import Configurator
    Configurator.apply(self, config["gateway"])

#    if self.id is None:
#      try:
#        import ubinascii
#      except ImportError:
#        import binascii as ubinascii 
#      try:
#        import uhashlib
#      except ImportError:
#        import hashlib as uhashlib
#      self.id = ubinascii.hexlify(uhashlib.sha256(machine.unique_id()).digest()).decode()

    self.topic = "/kiota/{}".format(self.id)
    self.last_ping = 0

    self.client = MQTTClient(self.topic,
                             self.mqtt_server.server,
                             self.mqtt_server.port,
                             self.mqtt_server.username,
                             self.mqtt_server.password,
                             self.mqtt_server.keep_alive)
    self.client.set_callback(self.do_message_callback)
    self.exit_topic = "{}/exit".format(self.topic)
    
    self.devices = []

    for d in config["devices"]:
    
      try:
        
        class_name =  d["type"]
        
        module_name = class_name
        try: module_name = d["module"]
        except (KeyError): pass

        package_name = "kiota"
        try: package_name = d["package"]
        except (KeyError): pass

        package = __import__("{}.{}".format(package_name, module_name), class_name)
#        print(package)
        module = getattr(package, module_name)
#        print(module)
        klass = getattr(module, class_name)
#        print(klass)
        
        device = klass(d)
        self.devices.append(device) 

      except ImportError as e:
        Util.log(self,"error: '{}' config: '{}'".format(e,d))


  def connect(self):
    self.client.connect()
    Util.log(self,"connect to MQTT server on {}:{} as {}".format(
        self.mqtt_server.server, 
        self.mqtt_server.port, 
        self.mqtt_server.username))
    self.subscribe(self.exit_topic)
    for device in self.devices: 
      device.connect(self)

  def subscribe(self, topic):
    self.client.subscribe(topic.encode())
        
  def publish(self, topic, payload):
    Util.log(self,"sent: topic '{}' payload: '{}'".format(topic,payload))
#    self.client.publish(topic.encode('utf-8'), payload)
    self.client.publish(topic.encode(), payload)
    
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
          time.sleep(self.mqtt_server.wait_to_reconnect)
      except IndexError as e:
          Util.log(self,"failed to connect, retrying....", e)
          time.sleep(self.mqtt_server.wait_to_reconnect)
  
    self.client.disconnect()
    
  def push(self):
    if time.time() > self.last_ping + self.mqtt_server.keep_alive/3:
      self.last_ping = time.time()
      self.client.ping()
    for device in self.devices: 
      device.push()
      
  def do_message_callback(self, b_topic, payload):
    topic = b_topic.decode() #convert to string
    
    import gc, micropython
    gc.collect()
    gc.threshold(gc.mem_free() // 4 + gc.mem_alloc())
    micropython.mem_info()

    Util.log(self,"received: topic '{}' payload: '{}'".format(topic,payload))
    if topic == self.exit_topic:
      raise ExitGatewayException()
    for device in self.devices: 
      if device.do_message(topic, payload):
#        Util.log(self,"consumed: topic '{}' payload: '{}' by device {}".format(topic,payload,json.dumps(device.config)))
#        break
        return        