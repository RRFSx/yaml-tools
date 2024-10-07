# yaml_tools

The YAML files are one of the core components of the JEDI system. Efficiently handling YAML files is crucial for utilizing JEDI in both research and operational development. We need simple, intuitive, and user-friendly YAML tools to help scientists easily examine, compare, manipulate, and breakdown/assemble YAML files.

Python offers [PyYAML module](https://pypi.org/project/PyYAML/), which is a powerful for developers to control details over YAML files. However, it comes with a learning curve and requires coding/debugging.

On the other hand, [`yq`](https://github.com/mikefarah/yq) a lightweight and portable command-line YAML, JSON and XML processor. While userful, it lacks a few key features that are essential for JEDI YAML file manipulation:   
1. JEDI YAML files often include spaces in key names, such as `cost function`, but currently, as far as I know, `yq` does not support handling spaces in key names.
2. `yq` does not provide a quick way to view top-level keys at the current nesting level.
3. `yq` does not support traverseing a YAML file to output a tree structure of its keys.

A PyYaml-based `yaml_tools` repository is developed to address the above limitations. This repo includes the following utilities:
### 1. `ycheck`
This script just load a yaml file and then dump data to stdout. If a yaml file contains non-standard elements, it will halt and provide detailed error information.   
`ycheck sample.yaml`
### 2. `yquery`
This script queries a given element using a query string.   
```
yquery sample.yaml ["key1/key2/0"] [shallow|traverse|dump|changeto=""]
```
- `shallow` is the default behavior which output the top level keys at the current nesting level
- The query string consists a series of keys (or index for lists) from the top level to the target level
- The "changto=" action is still under development (i.e. not ready for use)
### 3. `ybreakdonw`
This script breaks down a YAML file into individual elements, from top to bottom, and generates a corresponding directory tree. Each intermediate sub-YAML file is dumped into its respective directory, making it easy to examine the structure step by step.   
`ybreakdown sample.yaml`

# Mini Tutorial
This repository assumes the current Python environment has installed the `PyYAML` module.   
On NOAA RDHPCS, `PyYAML` can be find in the RDASApp `EVA` Python environment.
```
git clone https://github.com/NOAA-EMC/RDASApp
cd RDASApp
source ush/load_eva.sh
git clone https://github.com/rrfsx/yaml_tools.git
cd yaml_tools
```
### 1. ycheck
```
./ycheck samples/raw.mpasjedi_en3dvar.yaml
```
You will get the following error message:
```
...
  File "/lfs5/BMC/wrfruc/gge/miniconda3/4.6.14/envs/eva/lib/python3.9/site-packages/yaml/scanner", line 258, in fetch_more_tokens
    raise ScannerError("while scanning for the next token", None,
yaml.scanner.ScannerError: while scanning for the next token
found character '%' that cannot start any token
  in "samples/raw.mpasjedi_en3dvar.yaml", line 96, column 16
```
You can diff this file with `samples/mpasjedi_en3dvar.yaml` to see what changes can fix this error.
### 2. yquery
```
./yquery samples/rrfs_mpasjedi_2024052700_Ens3Dvar.yaml
./yquery samples/rrfs_mpasjedi_2024052700_Ens3Dvar.yaml "cost function"
./yquery samples/rrfs_mpasjedi_2024052700_Ens3Dvar.yaml "cost function/background"
./yquery samples/rrfs_mpasjedi_2024052700_Ens3Dvar.yaml "cost function/background" traverse
./yquery samples/rrfs_mpasjedi_2024052700_Ens3Dvar.yaml "cost function/background" dump > background.yaml
vi background.yaml
./yquery samples/rrfs_mpasjedi_2024052700_Ens3Dvar.yaml "cost function/observations/observers/0/obs filters/0/action" traverse
./yquery samples/rrfs_mpasjedi_2024052700_Ens3Dvar.yaml "cost function/observations/observers/0/obs filters/0/action" dump
```
### 3. ybreakdown
```
./ybreakdown samples/rrfs_mpasjedi_2024052700_Ens3Dvar.yaml
cd rrfs_mpasjedi_2024052700_Ens3Dvar.yaml/cost function/observations/observers
```
Under the `observers` subdirectory, you can see 16 observers and you can compare configurations from different observers.

