#!/bin/bash

PIPE=/tmp/netcheck_result

if [[ ! -p $PIPE ]]; then
  echo "Named pipe $PIPE does not exist"
  exit 1
fi

while true
do
  if read line <$PIPE;then
    if [["$line" == "quit";then
      break
    fi
    echo $line
  fi
done

echo "Reader exiting"
