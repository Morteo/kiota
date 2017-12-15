
# Implementation of Micropython umqtt.simple/umqtt/simple for Python 3
#   https://github.com/micropython/micropython-lib/blob/master/umqtt.simple/umqtt/simple.py
#   https://github.com/eclipse/paho.mqtt.python 

import paho.mqtt.client

class MQTTException(Exception):
    pass

class MQTTClient:

    def __init__(self, client_id, server, port=0, user=None, password=None, keepalive=0,
                 ssl=False, ssl_params={}):
        if port == 0:
            port = 8883 if ssl else 1883
        self.client_id = client_id
        
        self.server = server
        self.port = port
        self.keepalive = keepalive
        
        self.user = user
        self.pswd = password

        self.cb = None
        
        self.ssl = ssl
        self.ssl_params = ssl_params
        
        self.lw_topic = None
        self.lw_msg = None
        self.lw_qos = 0
        self.lw_retain = False

    def _on_message(self, client, userdata, msg):
      
      topic = msg.topic
      
      if isinstance(topic,str):
        topic = topic.encode("utf-8")
      
      payload = msg.payload
      
      if isinstance(payload,str):
        payload = payload.encode("utf-8")
        
#      print(" #### _on_message topic={}".format(topic))
#      print(" ####_on_message msg={}".format(payload))
      
      if userdata.cb is not None:
        userdata.cb(topic, payload)
    
    def set_callback(self, f):
        self.cb = f

    def set_last_will(self, topic, msg, retain=False, qos=0):
        
        self.lw_topic = topic
        self.lw_msg = msg
        self.lw_qos = qos
        self.lw_retain = retain
        
        self.client.will_set(topic, msg, qos, retain)

    def connect(self, clean_session=True):

        self.client =  paho.mqtt.client.Client(self.client_id, clean_session)
        self.client.user_data_set(self)
        self.client.on_message = self._on_message
      
        if self.user is not None:
          self.client.username_pw_set(self.user, self.pswd)
      
        self.client.connect(self.server, self.port, self.keepalive)
        
        if self.lw_topic is not None:
          set_last_will(self, self.lw_topic, self.lw_msg, self.lw_retain, self.lw_qos)

    def disconnect(self):
      self.client.disconnect()

    def ping(self):
      self.client.loop_misc()

    def publish(self, topic, msg, retain=False, qos=0):
      
      if isinstance(topic,bytes):
        topic = topic.decode("utf-8")
        
      if isinstance(msg,bytes):
        msg = msg.decode("utf-8")
        
#      print(" #### publish topic={}".format(topic))
#      print(" #### publish msg={}".format(msg))
      
      self.client.publish(topic, msg, qos, retain)

    def subscribe(self, topic, qos=0):
      
      if isinstance(topic,bytes):
        topic = topic.decode("utf-8")
        
#      print(" #### subscribe topic={}".format(topic))

      self.client.subscribe(topic, qos)

    # Wait for a single incoming MQTT message and process it.
    # Subscribed messages are delivered to a callback previously
    # set by .set_callback() method. Other (internal) MQTT
    # messages processed internally.
    def wait_msg(self):
      if self.keepalive > 0:
        timeout = self.keepalive
      else: 
        timeout = 1
      self.client.loop(timeout)      
      
    # Checks whether a pending message from server is available.
    # If not, returns immediately with None. Otherwise, does
    # the same processing as wait_msg.
    def check_msg(self):
      self.client.loop(0)
