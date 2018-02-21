import json
import time

class Device:
  
  id = None
  freq = None
  just_changes = False
  debounce = 0    
  
  last_push = 0
  last_payload = None

  def __init__(self, config):
    self.configure(config)
  
  def configure(self, config):
    from kiota.Configurator import Configurator
    Configurator.apply(self, config)
      
  def read(self):
    pass

  def write(self):
    pass
  
  def connect(self, gateway):
    
    self.gateway = gateway

    if self.id is not None:
      self.topic = "{}/{}".format(gateway.topic, self.id)
    else:
      self.topic = "{}/{}".format(gateway.topic, self.__class__.__name__)
      if self.gpio is not None:
        self.topic = "{}/{}".format(self.topic, str(self.gpio))
        
    payload = { 'connected': self.topic }
    self.gateway.publish(gateway.topic, json.dumps(payload))
      
#    self.gateway.subscribe("{}/configure".format(self.topic))
    self.gateway.subscribe("{}/get".format(self.topic))
    self.gateway.subscribe("{}/set".format(self.topic))
    
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

#    elif topic.endswith("/configure"):
#      
#      self.configure(payload)
#      return True

    return False

  def publish(self, payload):

    if payload is None:
      return
    
    if self.just_changes is False or payload != self.last_payload:
      try:
        self.gateway.publish(self.topic, json.dumps(payload))
      except Exception as e:
        import sys
        sys.print_exception(e)
      self.last_payload = payload

  def push(self):
                        
    if self.freq is None or self.freq < 0:
      return False
    
    if time.time() > self.last_push + self.freq:

      payload = self.read()
      
      if self.debounce > 0:
        for i in range(self.debounce,0,-1):
          time.sleep(0.01)
          if self.read() != payload:
#            import kiota.Util as Util
#            Util.log(self,"BOUNCE payload: '{}'".format( payload))
            return False

      self.publish(payload)
      self.last_push = time.time()
      return True
                        
    return False

