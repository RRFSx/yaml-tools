#!/bin/bash

if (( $# < 1 )); then
  echo "Usage: $0 yamlfile [enkf]"
  exit
fi

fpath=$1
if [[ "$2" == "enkf" ]]; then
  qstr="observations/observers"
else
  qstr="cost function/observations/observers"
fi

echo "empty" | yquery ${fpath} "${qstr}" edit=pipe | yquery pipe "test" delete > emptyobs.yaml
