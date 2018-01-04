
# Remember to remove the trailing \r if used in shell script 
# e.g
#     VAR=$(ampy --port $PORT run mycode.py | tr -d '\r')

import machine
import ubinascii
import uhashlib

print(ubinascii.hexlify(uhashlib.sha256(machine.unique_id()).digest()).decode())
