easy-pysy
==

# TODO:
## Features
- [ ] Doc : purpose, roadmap
- [ ] repo
- [ ] Daemon vs Run vs Start => BIG MESS RIGHT NOW
- [ ] Gui
  - [ ] Chrome web app
  - [ ] call_store_method => Real fastapi for serialization
  - [ ] index.html

# Getting Started
## Cheat sheet
```bash
# Install 
poetry install

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

## Publish
```bash
poetry publish --build
```