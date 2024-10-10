#!/bin/bash

if (( $# < 2 )); then
  echo "Usage: $0 <file1> <file2> [file3] ... [fileN]"
  exit
fi

file1=$1
shift
others=$@

qstr="cost function/observations/observers"
ymergeList ${file1} "${qstr}" ${others}
