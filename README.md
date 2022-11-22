easy-pysy
==

# TODO:
## Features
- [ ] Try/except with AppStopping
- [ ] Exception in app should stop uvicorn
- [ ] Error: Missing command => Still running !
- [ ] Doc : purpose, roadmap
- [ ] repo
- [ ] Daemon vs Run vs Start

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