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

# get the list size
nsize=$(yquery ${fpath} "${qstr}" | grep -o '[0-9]\+')
nsize=$(( nsize -1 ))

for i in $(seq 0 ${nsize}); do
  echo "====== $i"
  yquery ${fpath} "${qstr}/$i" dump > yamlobs.$i.yaml
  grep "is_in" yamlobs.$i.yaml
done
