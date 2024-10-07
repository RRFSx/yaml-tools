#!/usr/bin/env python
# POC: Guoqing.Ge@noaa.gov
#
import yaml, sys, os, shutil, glob

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

def breakDownYamlFile(data, fname):
  print('.', end='', flush=True)  # Print a dot without a newline so that users know the program is still running
  save_cwd=os.getcwd()
  with open(fname,'w') as yfile:
    yaml.dump(data, yfile, Dumper=MyDumper, default_flow_style=False, sort_keys=False)

  if isinstance(data,dict):
    for key,value in data.items():
      os.makedirs(key, exist_ok=True)
      os.chdir(key)
      newfname=f"{key}.yaml"
      breakDownYamlFile(value,newfname)
      os.chdir(save_cwd)
  elif isinstance(data,list):
    if all(isinstance(item, (str, int, float, bool)) for item in data): # list of leaves
      with open('list.txt', 'w') as myfile:
        for item in data:
          myfile.write(f"{item}\n")
    else: # list of dict/list
      for index, value in enumerate(data):
        with open("type_list",'w'):
          pass # create an empty file 'type_list' to indict a list under the current directory
        list_name=f'list_{index:02d}'
        os.makedirs(list_name,exist_ok=True)
        os.chdir(list_name)
        breakDownYamlFile(value,f"{list_name}.yaml")
        os.chdir(save_cwd)
  else:
    with open('leaf.txt','w') as myfile:
      if data is None:
        myfile.write('None')
      else:
        myfile.write(str(data))

# ====== main =========
MyDumper.add_representer(list, MyDumper.represent_list)
args=sys.argv
nargs=len(args)-1
if nargs <1:
  print(f"Usage: {args[0]} <file>")
  exit()
myfile=args[1]

with open(myfile) as yfile:
  data=yaml.safe_load(yfile)

basename=os.path.basename(myfile)
#if os.path.exists(basename):
#  shutil.rmtree(basename)
os.makedirs(basename, exist_ok=True)
os.chdir(basename)
breakDownYamlFile(data,basename)
print("")

files_to_move = glob.glob('_*')
os.makedirs("_anchors", exist_ok=True)
for myfile in files_to_move:
  shutil.move(myfile, './_anchors')
