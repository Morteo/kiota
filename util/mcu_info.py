import sys
import machine
import ubinascii
import uhashlib
import network

print("sys: ",sys.implementation)
print("uuid: ",ubinascii.hexlify(uhashlib.sha256(machine.unique_id()).digest()).decode())
print("mac: ",ubinascii.hexlify(network.WLAN().config('mac')).decode())