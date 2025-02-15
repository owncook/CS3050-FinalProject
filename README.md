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

## Building Desktop App (macOS)
> **Note:** The leaderboard function __**will not work**__ if you do not have a firebase key. To request one, email one of the creators.

First clone the repository to your device. Next, navigate to the repository directory and run:
```
    pyinstaller --onefile --windowed \
    --name "Galaga" \
    --icon=sources/app_icon/galaga.icns \
    --add-data "keys:keys" \
    --add-data "sources:sources" \
    main.py
```
Navigate into the newly built dist folder, then open the main folder. 
Inside are an _include folder and a main.exec. In order to run the exec from your desktop, transfer both the _include folder and the exec to your desktop. 
To launch, double click the exec!

## Getting Started

### Running

Download the zip archive of the app and start playing!

Alternativley, run the [main.py](main.py) script from the repo directory.

### Controls

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
