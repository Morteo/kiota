
from machine.Pin import Pin

def unique_id():
  import uuid
  return uuid.getnode()