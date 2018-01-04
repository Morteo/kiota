#!/usr/bin/env bash

echo "::: Backing up KIOTA files :::"

KIOTA=~/working/kiota
PORT=/dev/ttyUSB0

MAC=$(ampy --port $PORT run ${KIOTA}/util/mcu_mac.py | tr -d '\r')
SECS=$(date +%s )
BACKUP_DIR="kiota_${SECS}_${MAC}"

echo "to folder $BACKUP_DIR"

mkdir $BACKUP_DIR

cd $BACKUP_DIR

ampy --port $PORT run ${KIOTA}/util/mcu_info.py > mcu_version.txt

for i in $( ampy --port $PORT ls ); do
  echo file: $i
  ampy --port $PORT get $i $i
done

mkdir dg_mqtt
cd dg_mqtt
for i in $( ampy --port $PORT ls /dg_mqtt); do
  echo file: /dg_mqtt/$i
  ampy --port $PORT get /dg_mqtt/$i $i
done

cd ..
mkdir config
cd config
for i in $( ampy --port $PORT ls /config); do
  echo file: /config/$i
  ampy --port $PORT get /config/$i $i
done

cd ..

exit
