import time
import ubinascii
import uhashlib
import network
import machine
import sys
from umqtt.simple import MQTTClient
from dg_mqtt.Device import Device
from dg_mqtt.Util import Log
from dg_mqtt.Util import ConfigFile

class ExitGatewayException(Exception):
    pass

class Gateway:
 
  default_config = {
    'version': 2,
    'server': '127.1.1.1',
    'port': 1883,
    'keep_alive': 60,
    'wait_to_reconnect': 5,
    'username': None,
    'password': None
  }
  
  last_ping = 0

  def __init__(self, config):

    self.config = self.default_config.copy()
    self.config.update(config["Gateway"])
    self.devices = []

    if self.config['id'] is None:
      self.config['id'] = ubinascii.hexlify(uhashlib.sha256(machine.unique_id()).digest()).decode()

    if self.config['version'] is None:
        self.topic = "/devices/" +ubinascii.hexlify(network.WLAN().config('mac')).decode() + "/esp8266"
    else:
        self.topic = "/devices/" + self.config['id']

    self.client = MQTTClient(self.topic, self.config['server'], self.config['port'], self.config['username'], self.config['password'], self.config['keep_alive'])
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
        Log.log(self,"error: '{}' config: '{}'".format(e,device_config))


  def connect(self):
    self.client.connect()
    Log.log(self,"connect to MQTT server on {}:{} as {}".format(self.config['server'], self.config['port'], self.config['username']))
    self.subscribe(self.exit_topic)
    for device in self.devices: 
      device.connect(self)

  def subscribe(self, topic):
    self.client.subscribe(topic.encode())
#    time.sleep(0.01) # attempt to reduce number of OSError: [Errno 104] ECONNRESET 
        
  def publish(self, topic, payload):
    Log.log(self,"publish topic: '{}' payload: '{}'".format(topic,payload))
    self.client.publish(topic.encode('utf-8'), payload)
#    time.sleep(0.01) # attempt to reduce number of OSError: [Errno 104] ECONNRESET 
    
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
          Log.log(self,"failed to connect, retrying....", e)
          time.sleep(self.config["wait_to_reconnect"])

    self.client.disconnect()
    
  def main(config_filename):
    try:
      config = ConfigFile(config_filename).config
      Gateway(config).start()
    except Exception as e:
      import sys
      sys.print_exception(e)
    
  def push(self):
    if time.time() > self.last_ping + self.config["keep_alive"]/3:
      self.last_ping = time.time()
      self.client.ping()
    for device in self.devices: 
      device.push()
      
  def do_message_callback(self, b_topic, payload):
    topic = b_topic.decode() #convert to string
    Log.log(self,"message received: '{}' payload: '{}'".format(topic,payload))
    if topic == self.exit_topic:
      raise ExitGatewayException()
    for device in self.devices: 
      if device.do_message(topic, payload):
        break
        