
# Remember to remove the trailing \r if used in shell script 
# e.g
#     VAR=$(ampy --port $PORT run mycode.py | tr -d '\r')

import sys

print(sys.implementation)
