from distutils.core import setup

import py2exe
import glob

setup(
    console=["main.py"],
    data_files=[
        ("sprites", glob.glob("assets/settings\\*.json")),
        ("sound", glob.glob("assets/sound\\*.ogg") + glob.glob("assets/sound\\*.wav")),
        ("levels", glob.glob("assets/levels\\*.json")),
        ("images", glob.glob("assets/images\\*.gif") + glob.glob("assets/images\\*.png")),
        ("", ["settings.json"]),
    ],
)
