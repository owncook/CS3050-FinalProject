# CS3050 Group 3 Final Project: Galaga

### Introduction

This is group 3's CS3050 Software Engineering final project. With the use of python arcade we set out to make our version of the classic arcade game Galaga.

# Authors

- Owen Cook
- Elizabeth Lembach
- Tucker Schulz
- Cam Wodarz

## Installation

Clone the repository to your device and navigate to it via ide or terminal.

The [PythonArcade's](https://api.arcade.academy/en/latest/examples/platform_tutorial/step_01.html) install tutorial reccomended using a virtual environment to discourage package version conflicts. During our work we used/test venv and conda environments, pick your preference and activate it. To install the python arcade module navigate to terminal and run this command:

```
pip install arcade
```

## Optional Desktop Application Install
After cloning the repository to your device, run:
    pyinstaller main.py \
    --add-data "keys:keys" \
    --add-data "sources:sources" \
    --collect-data arcade
in the repo directory. Navigate into the newly built dist folder, then open the main folder. 
Inside are a _include folder and a main.exec. In order to run the exec from your desktop, transfer both the _include folder and the exec to your desktop. 
To launch, double click the exec!

## Getting Started

#### Running

If installed via the executeable run that or if cloned run the [main.py](main.py) script.

#### Controls

- Move left/right: left arrow button/right arrow button
- Fire bullet: Spacebar (you only get two at a time)

## More Info

### Dependencies

Below are PythonArcade's dependencies which are installed with the module. They are also present in our repo here: [requirements.txt](requirements.txt)

```
arcade==2.6.17
attrs==24.2.0
cffi==1.17.1
Pillow==9.3.0
pycparser==2.22
pyglet==2.0.dev23
pymunk==6.4.0
pytiled-parser==2.2.0
typing_extensions==4.12.2
```

### Known Bugs

```
AttributeError: ObjCInstance b'__NSSingleObjectArrayI' has no attribute b'type'
```

This is an error within arcade's required package pyglet and its interaction with MacOS. It appears to be fixed in the newer versions of pyglet, however arcade specifies the v2.0.dev23 release from May 2022. More information on the bug can be found [here](https://github.com/pyglet/pyglet/releases?q=v2.0.dev23&expanded=true).
