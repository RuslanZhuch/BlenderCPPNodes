# BlenderCPPNodes
Custom Blender nodes tree for C++ code generation.

![Nodes header example](https://github.com/RuslanZhuch/BlenderCPPNodes/blob/main/repoMedia/TemplateHeader.JPG?raw=true)

## Features
- generate custom nodes from user provided json files
- generate c++ code from constructed trees

## Getting started

### Requirements
- Blender https://www.blender.org/ (3.4 is preferred) 
- A folder with structure:
```
root/
├─ nodes-structures/
├─ sources/
├─ nodesOutput/
│  ├─ temp/
│  ├─ generated/
├─ genschemas.sh

```
genschemas.sh is a user provider script that generates json schemas and puts them to
"nodes-structures" folder.

### Installation
- Install blender
- Clone this repository to "user/AppData/Roaming/Blender Foundation/Blender/<blender version>/scripts/addons"
- Open blender, go to Edit -> Prefernces -> Add-ons, check "Community", find and activate "Rising: cppGen"

Now you must be able to open Scripting editor.

## Usage
### Quick start

Create a json file in your "nodes-structures" folder
```json
[
    {
        "type": "namespace",
        "name": "Blocks",
        "members": [
            {
                "type": "namespace",
                "name": "Math",
                "members": [
                    {
                        "type": "function",
                        "returnType": {
                            "name": "float"
                        },
                        "name": "sigma",
                        "arguments": [
                            {
                                "type": {
                                    "name": "auto"
                                },
                                "name": "t"
                            }
                        ]
                    }
                ]
            }
        ]
    }
]
```
Outer scope is an array of namespaces. Every group of blocks must be 
contained within a namespace "Blocks". Group is a namespace with an arbitary name.
In this example we have one group "Math", which contains a function "sigma".

The function has a return value of type "float" and a parameter "t" of type "auto".

To generate nodes, open right-hand toolbar in the tree editor and navigate to Misc tab.
Select your directory and press Generate nodes button. 

Now you must be able to create three nodes:
- Input and Output nodes in I/O groupt;
- sigma node in Math group.

![Three nodes example](https://github.com/RuslanZhuch/BlenderCPPNodes/blob/main/repoMedia/Sample1Nodes.JPG?raw=true)

Create the node tree shown above and press "Parse nodes" button. 
This process will generate two files in your "nodesOutput" folder:
- generationIncludes.h - includes all your custom code header files. This list 
is created from names of the same json files used for nodes generation.
- <your node tree name>.h - c++ generated code from the nodes tree.

Generated code example
```c++
#pragma once
#include "generationIncludes.h"

auto NodeTree(auto&& arg1)
{
    const auto sigmaResult{ Blocks::Math::sigma(arg1) };

    struct OutS
    {
        decltype(sigmaResult) out1;
    };
    return OutS(sigmaResult);
}
```

### User defined types

You can provide a custom output type.

Type is an object within a namespace Types. Object must have a f "type": "class".
Basically type is a c++ class or struct.
```json
[
    {
        "type": "namespace",
        "name": "Types",
        "members": [
            {
                "type": "class",
                "name": "Vec2",
                "members": [
                    {
                        "type": "property",
                        "dataType": {
                            "name": "int"
                        },
                        "name": "x"
                    },
                    {
                        "type": "property",
                        "dataType": {
                            "name": "int"
                        },
                        "name": "y"
                    }
                ]
            }
        ]
    }
]
```
A User-defined type must be refferenced as shown below.
```json
"returnType": {
    "type": "literal",
    "name": "Types::Vec2"
},
```

![Type nodes example](https://github.com/RuslanZhuch/BlenderCPPNodes/blob/main/repoMedia/Sample2Nodes.JPG?raw=true)

### Pre-release version
This is a pre-release version of the library. 

Roadmap:
- Socket connection check;
- Global grouping;
- Local grouping;
- Caching;
- Debug tools;
