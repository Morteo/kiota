import time
import ubinascii
import network
from umqtt.simple import MQTTClient
from dg_mqtt.Devices import Device
from dg_mqtt.Util import Log
from dg_mqtt.Util import ConfigFile

class ExitGatewayException(Exception):
    pass

class Gateway:
 
  default_config = {
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
    
#    self.client_id = "/devices/esp8266_" + ubinascii.hexlify(machine.unique_id()).decode()
    self.client_id = "/devices/" + ubinascii.hexlify(network.WLAN().config('mac')).decode() + "/esp8266"
    self.client = MQTTClient(self.client_id, self.config['server'], self.config['port'], self.config['username'], self.config['password'], self.config['keep_alive'])
    self.client.set_callback(self.do_message_callback)
    self.exit_topic = self.client_id+"/Gateway/exit"
    
    
    for dconfig in config["Devices"]:
      device = Device.initDevice(dconfig)
      self.devices.append(device)  

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
          self.do_push()
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
    
  def do_push(self):
    if time.time() > self.last_ping + self.config["keep_alive"]/3:
      self.last_ping = time.time()
      self.client.ping()
    for device in self.devices: 
      device.do_push()
      
  def do_message_callback(self, b_topic, payload):
    topic = b_topic.decode() #convert to string
    Log.log(self,"message received: '{}' payload: '{}'".format(topic,payload))
    if topic == self.exit_topic:
      raise ExitGatewayException()
    for device in self.devices: 
      if device.do_message(topic, payload):
        break
