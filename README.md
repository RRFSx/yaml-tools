YAML files are a key component of the JEDI system. Efficient handling of these files is crucial for both research and operational development within JEDI. To support this, we need simple, intuitive, and user-friendly command-line tools that allow scientists to easily examine, compare, manipulate, and break down or assemble YAML files.

Python's [PyYAML module](https://pypi.org/project/PyYAML/) offers powerful functionality for developers, enabling detailed control over YAML file handling. However, it comes with a learning curve and requires coding and debugging.

Alternatively, [`yq`](https://github.com/mikefarah/yq) a lightweight and portable command-line YAML, JSON and XML processor. While useful, it lacks a few key features that are essential for working with JEDI YAML files:   
* JEDI YAML files often include spaces in key names, such as `cost function`, but currently, as far as I know, `yq` does not support handling spaces in key names.
* `yq` does not provide a easy way to view top-level keys at the given nesting level.
* `yq` does not support traversing a YAML file to output a tree structure of its keys.

A PyYaml-based `yaml-tools` repository is developed to address the above limitations. This repo includes the following utilities:

### NOTE:
* `< >` means `required`
* `[ ]` means `optional`
* `|` means `or`
* `querystr` refers to a string which describes the path from the top level key (or index, if a list) to the destination level key (or index). It uses `/` to separate different keys/indices. Let's use the following YAML file as an example:
```
demo:
  configuration:
    suite: YAML
    detail:
      - meaning:
        - Y: Yelling
        - A: At
        - M: My
        - L: Laptop
```
So a query string `"demo/configuration/detail/0/meaning"` will return a list of 4 items and the value is as follows:
```
- Y: Yelling
- A: At
- M: My
- L: Laptop
```

### 1. `ycheck <file> [dump]`
This script loads a YAML file and prints its content to stdout. If the YAML file contains any non-standard elements, the script will stop and display detailed error information. Otherwise, it will output the contents in the form of a Python dictionary or list.

Additionally, you can use the optional `dump` command-line option to output the content in standard YAML format instead.

### 2. `yquery`
```
yquery <pipe|file> [querystr] [traverse|dump|edit=|append=|delete]
```
This script queries a specific element in a YAML file using a query string.   
- `pipe`: Reads YAML data from the system's standard input, allowing this command to be used in command-line piping.
- `file`: Read YAML data from a file, e.g. `yquery ./mini01.yaml`
- `querystr`: The query string used to locate the desired element. If not provided, it defaults to an empty string, which refers to the full YAML content at the topmost level.
- `traverse|dump|edit=|append=|delete`: These are the actions that can be performed on the element specified by the query string. 
    
If no action is specified, `yquery` will print the keys or list size at the level specified by the query string.
- `traverse`: Navigates through the nested structure of the YAML data, starting at the level defined by the query string and descending into sub-elements until reaching the leaf elements.
- `dump`: Outputs the YAML content specified by the query string in standard YAML format.
- `edit=<pipe|file|string>`: Modifies the value of the YAML element at the location defined by the query string. If the value is a dictionary or list, the new value is read from standard input (e.g., via piping) or another YAML file. For literals, the new value is specified directly after the = sign.
- `append=<pipe|file>`: Adds a new key to a dictionary or an item to a list at the level specified by the query string. The value to append is read from standard input or another YAML file. No changes are made if the query string refers to a literal.
- `delete`: Removes a key from a dictionary or an item from a list at the level defined by the query string.

### 3. `ybreakdown <file>`
This script breaks down a YAML file into individual elements, top to bottom, and generates a corresponding directory tree. Each intermediate sub-YAML file is dumped into its respective directory, making it easy to explore the YAML file structure step by step.   

### 4. `ymergeList <file1> <querystr> <file2> [file3]...[fileN]`
This script allows you to merge multiple YAML files into one by combining the lists specified by the query string. It assumes that all files share the same structure up to the destination level. The lists from the other files are merged into the `file1` YAML data and the result is output to stdout. This functionality is particularly useful for combining different `observations/observers` from various types of observations.

### 5. Tutorial ([Click here](https://github.com/rrfsx/yaml-tools/wiki/YAML%E2%80%90TOOLS-tutorial))

Feel free to contact Guoqing.Ge at noaa.gov for any questions/comments.

