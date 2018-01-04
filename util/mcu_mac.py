
# Remember to remove the trailing \r if used in shell script 
# e.g
#     VAR=$(ampy --port $PORT run mycode.py | tr -d '\r')


import ubinascii
import uhashlib
import network
print(ubinascii.hexlify(network.WLAN().config('mac')).decode())
