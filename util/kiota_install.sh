#!/usr/bin/env bash

KIOTA=.
PORT=/dev/ttyUSB0
DEVICE=example
SECRETS=$KIOTA/devices/__secrets__.py

usage()  
{  
  echo "Installs KIOTA on a microcontroller"
  echo "Usage: $(basename "$0") -p [port] -k [KIOTA] -d [device] -s [secrets_file] -c [config_file]"
  echo "where:"
  echo "  [port] is the port used to connect to the remote microcontroller (default: /dev/ttyUSB0)"
  echo "  [KIOTA] is the directory where KIOTA is installed (default: .)"
  echo "  [device] is the device name used to identify the configuration folder to be used (default: example)"
  echo "  [secrets_file] is the secret configuration file (default: ./devices/__secrets__.py)"
  echo "  [config_folder] is the device configuration fodler that containts config.py and overrides [device] (default: ./devices/example)"
  echo ""
  echo "e.g. $(basename "$0") -d example"
  echo ""
  exit 1  
} 

while [ "$1" != "" ]; do
  case $1 in
    -p | --port )
        shift
        PORT=$1
        ;;
    -k | --KIOTA )
        shift
        KIOTA=$1
        ;;
    -d | --device )
        shift
        DEVICE=$1
        ;;
    -s | --secrets )
        shift
        SECRETS=$1
        ;;
    -c | --config )
        shift
        CONFIG=$1
        DEVICE=""
        ;;
    * ) 
      echo "Unknown option: $1"
      usage
      
  esac
  shift
done

if [ -n "${DEVICE}" ] && [ -n "${CONFIG}" ] ; then
      echo "Option error: specfiy either -d or -c not both"
      usage
fi

if [ -z "${CONFIG+set}" ]; then
  CONFIG=$KIOTA/devices/$DEVICE/
else
  DEVICE="<none>"
fi

# Copy KIOTA micropython 
echo "::: Installing KIOTA on remote device :::"
echo "  on port: $PORT"
echo "  device: $DEVICE"
echo "  with device configuration: $CONFIG"
echo "  and secrets: $SECRETS"

echo "::: Remote device information :::"
(
  set -x #echo on
  ampy --port $PORT run $KIOTA/util/mcu_port_diag.py
  ampy --port $PORT run $KIOTA/util/mcu_sys.py
)

echo "::: Wipe the remote device :::"
read -p " Delete all files on the remote device (y/n)?" choice
case "$choice" in 
  y|Y )
    echo "    Wiping"
    # ampy --port $PORT run $KIOTA/util/factory_reset.py
    # 'os.mkfs() - not supported
    # Try rm root directory to delete all files. Works ok but generates an error so suppress
    ampy --port $PORT rmdir / &>/dev/null
    ;;
  * ) 
    echo "    Skipping wipe"
    ;;
esac

echo "::: Remote device free file space :::"
(
  set -x #echo on
  ampy --port $PORT run $KIOTA/util/mcu_df.py
)

function ampy_put_recursive()
{

  if [ "$2" != "/" ]; then
  (
    set -x #echo on
    ampy --port $PORT mkdir ${2%/}
  )
  fi
  
  for i in $( ls $1 -p ); do
    (
      case "$i" in
      __pycache__/)
          echo "    Skipping $i"
          ;;
      *.yaml)
          echo "    Skipping $i"
          ;;
      */)
          ampy_put_recursive $1$i $2$i
          ;;
      *)
          (
            set -x #echo on
            ampy --port $PORT put $1$i $2$i
          )
          ;;
      esac    
    )
  done
}

echo "::: Adding the device configuration and secrets :::"
(
  set -x #echo on
  ampy --port $PORT put $SECRETS
)
ampy_put_recursive $CONFIG /

echo "::: Adding the KIOTA files :::"


ampy_put_recursive $KIOTA/src/micropython/ /
ampy_put_recursive $KIOTA/src/kiota/ /kiota/

echo "::: Remote device free file space :::"
(
  set -x #echo on
  ampy --port $PORT run $KIOTA/util/mcu_df.py
)

echo "::: Reset micropython on the remote device :::"
read -p " (h)ard, (s)oft or (n)o reset ?" choice
case "$choice" in 
  h|H )
    (
      echo "    Hard Reset"
      set -x #echo on
      ampy --port $PORT run $KIOTA/util/hard_reset.py
    )
    ;;
  s|S ) 
    (
      echo "    Soft Reset"
      set -x #echo on
      ampy --port $PORT run $KIOTA/util/soft_reset.py
    )
    ;;
  * ) 
    echo "    No Reset"
    ;;
esac

echo "::: Remote device memory information :::"
(
  set -x #echo on
  ampy --port $PORT run $KIOTA/util/mcu_mem_info.py
)

echo "::: Done :::"

exit
