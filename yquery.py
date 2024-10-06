#!/usr/bin/env python
import yaml
import sys

# Custom Dumper class to modify list formatting
class MyDumper(yaml.Dumper):
  def represent_list(self, data):
    # Check if the list contains only simple literals (strings, numbers, booleans)
    if all(isinstance(item, (str, int, float, bool)) for item in data):
      # Use compact flow style ([])
      return self.represent_sequence('tag:yaml.org,2002:seq', data, flow_style=True)
    else:
      # Use block style (-)
      return self.represent_sequence('tag:yaml.org,2002:seq', data, flow_style=False)

def traverse(subdata,n): # traverse the yaml dict tree until reaching leafs
  n=n+1
  if isinstance(subdata,dict):
    for key,value in subdata.items():
      print(f"{' '*(n-1)*3}{key}")
      traverse(value,n)
  elif isinstance(subdata,list):
    print(f"{' '*n*3}[a list of {len(subdata)} item(s)]")
    for item in subdata:
      traverse(item,n)

def getFinalValue(subdata,keytree): # get the value for a hirearchy key string
  if keytree: # not empty
    if isinstance(subdata,dict):
      subdata=subdata[keytree.pop(0)]
    elif isinstance(subdata,list):
      index=int(keytree.pop(0))
      if index <0: 
        index=0
      elif index >= len(subdata):
        index=len(subdata)-1
      subdata=subdata[index]
    if not keytree: # if empty now
      return subdata
    else:
      return getFinalValue(subdata,keytree)

# ====== main =========
MyDumper.add_representer(list, MyDumper.represent_list)
args=sys.argv
nargs=len(args)-1
if nargs <1:
  print(f"Usage: {args[0]} <file> [keystr] [traverse|dump|changeto=''] #default action is traverse")
  exit()
myfile=args[1]
mykeystr=""
if nargs >1:
  mykeystr=args[2]
action="traverse"
if nargs>2:
  action=args[3]

with open(myfile) as yfile:
  data=yaml.safe_load(yfile)

if mykeystr:
  keytree=mykeystr.split("/")
  subdata=(getFinalValue(data,keytree))

  if action=="traverse":
    traverse(subdata,0)
  elif action=="dump":
    if isinstance(subdata,dict):
      yaml.dump(subdata, sys.stdout, Dumper=MyDumper, default_flow_style=False, sort_keys=False)
      #yaml.dump(subdata, sys.stdout, default_flow_style=True)
      #yaml.dump(subdata, sys.stdout)
    elif isinstance(subdata,list):
     print(f'[a list of {len(data)} item(s)]')
    else:
      print(subdata)
else:
  # list the top-level keys or times
  if isinstance(data, dict):
    for key in data.keys():
      print(f"{key}")
  elif isinstance(data,list):
     print(f'[a list of {len(data)} item(s)]')
