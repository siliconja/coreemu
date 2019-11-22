import logging
import os
import shutil
from pathlib import Path

import yaml

# gui home paths
from coretk import themes

HOME_PATH = Path.home().joinpath(".coretk")
BACKGROUNDS_PATH = HOME_PATH.joinpath("backgrounds")
CUSTOM_EMANE_PATH = HOME_PATH.joinpath("custom_emane")
CUSTOM_SERVICE_PATH = HOME_PATH.joinpath("custom_services")
ICONS_PATH = HOME_PATH.joinpath("icons")
MOBILITY_PATH = HOME_PATH.joinpath("mobility")
XML_PATH = HOME_PATH.joinpath("xml")
CONFIG_PATH = HOME_PATH.joinpath("gui.yaml")

# local paths
LOCAL_ICONS_PATH = Path(__file__).parent.joinpath("icons").absolute()
LOCAL_BACKGROUND_PATH = Path(__file__).parent.joinpath("backgrounds").absolute()

# configuration data
TERMINALS = [
    "$TERM",
    "gnome-terminal --window --",
    "lxterminal -e",
    "konsole -e",
    "xterm -e",
    "aterm -e",
    "eterm -e",
    "rxvt -e",
    "xfce4-terminal -x",
]
EDITORS = ["$EDITOR", "vim", "emacs", "gedit", "nano", "vi"]


class IndentDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)


def check_directory():
    if HOME_PATH.exists():
        logging.info("~/.coretk exists")
        return
    logging.info("creating ~/.coretk")
    HOME_PATH.mkdir()
    BACKGROUNDS_PATH.mkdir()
    CUSTOM_EMANE_PATH.mkdir()
    CUSTOM_SERVICE_PATH.mkdir()
    ICONS_PATH.mkdir()
    MOBILITY_PATH.mkdir()
    XML_PATH.mkdir()
    for image in LOCAL_ICONS_PATH.glob("*"):
        new_image = ICONS_PATH.joinpath(image.name)
        shutil.copy(image, new_image)
    for background in LOCAL_BACKGROUND_PATH.glob("*"):
        new_background = BACKGROUNDS_PATH.joinpath(background.name)
        shutil.copy(background, new_background)

    if "TERM" in os.environ:
        terminal = TERMINALS[0]
    else:
        terminal = TERMINALS[1]
    if "EDITOR" in os.environ:
        editor = EDITORS[0]
    else:
        editor = EDITORS[1]
    config = {
        "preferences": {
            "theme": themes.DARK,
            "editor": editor,
            "terminal": terminal,
            "gui3d": "/usr/local/bin/std3d.sh",
        },
        "servers": [{"name": "example", "address": "127.0.0.1", "port": 50051}],
        "nodes": [],
        "observers": [{"name": "hello", "cmd": "echo hello"}],
    }
    save(config)


def read():
    with CONFIG_PATH.open("r") as f:
        return yaml.load(f, Loader=yaml.SafeLoader)


def save(config):
    with CONFIG_PATH.open("w") as f:
        yaml.dump(config, f, Dumper=IndentDumper, default_flow_style=False)