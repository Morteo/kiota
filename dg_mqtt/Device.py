import json
import time

class Device:
  
  last_push = 0
  last_payload = None
  default_config = {
    "id": None,
    "description": None,
    "poll_frequency": None,
    "publish_changes_only": False
  }
  
  def __init__(self, config):
    self.configure(config)
  
  def configure(self, config):
    self.config = Device.default_config.copy()
    self.config.update(self.default_config)
    self.config.update(config)
      
  def read(self):
    pass

  def write(self):
    pass
  
  def connect(self, gateway):
    
    self.gateway = gateway

    if self.config['id'] is not None:
      self.topic =  gateway.topic + "/" + self.config['id']
    else:
      self.topic =  gateway.topic + "/" + self.__class__.__name__
      if self.config['gpio'] is not None:
        self.topic =  self.topic + "/" + str(self.config["gpio"])
        
    payload = { 'connected': self.topic }
    self.gateway.publish(gateway.topic, json.dumps(payload))
      
    self.gateway.subscribe(self.topic+"/configure")
    self.gateway.subscribe(self.topic+"/get")
    self.gateway.subscribe(self.topic+"/set")
    
  def do_message(self, topic, b_payload):

    if not(topic.startswith(self.topic)):
      return False

    payload = b_payload.decode().lower()

    if topic.endswith("/get"):

      self.publish(self.read())
      return True
                        
    elif topic.endswith("/set"):
      
      self.publish(self.write(payload))
      return True

    elif topic.endswith("/configure"):
      
      self.configure(payload)
      return True

    return False

  def publish(self, payload):

    if payload is None:
      return
    
    if self.config["publish_changes_only"] is False or payload != self.last_payload:
      try:
        self.gateway.publish(self.topic, json.dumps(payload))
      except Exception as e:
        import sys
        sys.print_exception(e)
      self.last_payload = payload

  def push(self):
                        
    if self.config["poll_frequency"] is None or self.config["poll_frequency"] < 0:
      return False
    
    if time.time() > self.last_push + self.config["poll_frequency"]:

      self.last_push = time.time()
      self.publish(self.read())

      return True
                        
    return False

