#!/usr/bin/env python
import yaml, sys, os

def breakDownYamlFile(data, fname)
  if isinstance(data,dict):
    for key,value in data.items():
      with open(fname,'w') as yfile:
        yaml.dump(data,yfile)
      os.makedirs(key, exist_ok=True)
      os.chdir(key)
      breakDownYamlFile(value,key)
  else isinstance(data,list):

  
  
  if keytree: # not empty
    subdata=subdata[keytree.pop(0)]
    if not keytree: # if empty now
      return subdata
    else:
      return getFinalValue(subdata,keytree)

# ====== main =========
args=sys.argv
nargs=len(args)-1
if nargs <1:
  print(f"Usage: {args[0]} <file>")
  exit()
myfile=args[1]

with open(myfile) as yfile:
  data=yaml.safe_load(yfile)

os.makdirs(myfile, exist_ok=True)
os.chdir(myfile)
for key,subdata in data.items():
  os.makedirs(key, exist_ok=True)
  os.chdir(key)
  subdata=(getFinalValue(data,keytree))

  if action=="traverse":
    traverse(subdata,0)
  elif action=="dump":
    yaml.dump(subdata, sys.stdout)

else:
  # list the top-level keys
