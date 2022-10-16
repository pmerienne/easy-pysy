easy-pysy
==

# TODO:
## Features
- [x] ~~ioc~~
- [x] loop
- [x] bus
- [x] pet_clinic
- [ ] config from .env
- [ ] examples outside
- [ ] hello_world example
- [ ] logger
- [ ] repo
- [ ] Poetry project structure
- [ ] Daemon vs Run vs Start

# Getting Started
## Folder structure
```tree
pyproject.toml
modules/
├── module_1.py
├── module_2.py
plugins/
├── plugin_1.py
├── plugin_2.py
```

## Cheat sheet
```bash
# Install 
poetry install

# Launch TODO: is it needed ?
ez start

# Run command
ez run <command>
```

# Dev Guide
## Install

```bash
# Install a python 3.9 version
pyenv install --list | grep " 3.9"
pyenv install -v 3.9.14

# Install dependencies
sudo apt install python3-poetry python3-venv python3-cachecontrol

# Install libs
poetry install

```


## Technical debt
- [ ] Cache for registered stuff ? <=> Repo ?
- [ ] Better separation app and root plugins ?
- [ ] cleanup model : EzLoop#component_function
- [ ] cleanup model : More in plugins ?