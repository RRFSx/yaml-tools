#!/bin/bash

if (( $# < 2 )); then
  echo "Usage: $0 yaml_file obs_file [enkf]"
  exit
fi

fpath=$1
fobs=$2
if [[ "$3" == "enkf" ]]; then
  qstr="observations/observers/0"
else
  qstr="cost function/observations/observers/0"
fi

yquery ${fpath} "${qstr}" edit=${fobs}
