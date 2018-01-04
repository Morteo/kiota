#!/usr/bin/python3
import json
from dg_mqtt.Gateway import Gateway

try:
  Gateway().start()
except Exception as e:
  import sys
  import traceback
  traceback.print_exception(None, e, sys.exc_info()[2])
