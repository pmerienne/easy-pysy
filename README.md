easy-pysy
==

# TODO:
- [x] Fast API => inside
- [x] CLI => inside
- [ ] UI

- [ ] CLEANUP
  - [ ] Plugins !
  - [ ] Configuration = Plugin(config=frfrf) instead of Plugin ?
- [ ] Daemon vs Run vs Start
- [ ] Doc : purpose, roadmap
- [ ] repo

**Bugs**
- [ ] Multiple static
- [ ] Pet -> save /cancel multiple !!
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