#!/usr/bin/python

import sys
import os
import getopt

from datetime import datetime
import RPi.GPIO as GPIO
import json

def record(gpio, loops, threshold, outfilepath):

  GPIO.setmode(GPIO.BCM)
  GPIO.setup(gpio, GPIO.IN)

  now = datetime.utcnow
  
  timings = []
  values = []
  last_value = None #GPIO.input(gpio)
  new_value = None #last_value

  print('Recording GPIO {} for {} times with threshold {}'.format(gpio, loops, threshold))
  
  for t in range(loops):
    new_value = GPIO.input(gpio)
    if new_value != last_value:
      timings.append(now())
      values.append(new_value)
      last_value = new_value

  GPIO.cleanup()

  print('Writing to file: {}'.format(outfilepath))

  try:
    with open(outfilepath, "w") as f:
      f.write('gpio,count,time,duration,value\n')
  
      print('len(timings): {}'.format(len(timings)))

      if len(timings)>0:
        
        start_time = timings[0]
        
        for i in range(len(timings)):
          timings[i] = int((timings[i] - start_time).total_seconds() * 1000000)
          if i == 0 :
            duration = 0
          else:
            duration = timings[i] - timings[i-1]
          if duration >= threshold: 
            f.write('{},{},{},{},{}\n'.format(gpio,i,timings[i],duration,values[i]))
  except OSError:
    print('failed to save to file: {}'.format(outfilepath))
  
  
def main(argv):
  
  usage = 'usage: -g <GPIO pin number> -l <number of loops> -l <threshold> -o <csv output file>'
  
  gpio = 27
  loops = 1000000
  threshold = 0
  outfile = ''
  
  try:
      opts, args = getopt.getopt(argv,"hg:l:t:o:",["gpio=","loops=","threshold=","ofile="])
  except getopt.GetoptError:
    print usage
    sys.exit(2)
    
  for opt, arg in opts:
    if opt == '-h':
      print usage
      sys.exit()
    elif opt in ("-o", "--ofile"):
      outfile = arg
    elif opt in ("-g", "--gpio"):
      gpio = int(arg)
    elif opt in ("-l", "--loops"):
      loops = int(arg)
    elif opt in ("-t", "--threshold"):
      threshold = int(arg)
        
  record(gpio, loops, threshold, outfile)
   

if __name__ == "__main__":
  main(sys.argv[1:])  
  
  
  
  