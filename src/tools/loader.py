'''
File: loader.py
Project: tools
File Created: Saturday, 29th February 2020 1:44:04 pm
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Saturday, 29th February 2020 2:23:18 pm
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''

import json
from pathlib import Path
from typing import List

def load_timesteps(dir: Path = Path("data/in")) -> List[dict]:
    """
    Loads .json files from the given directory for timestep data
    """
    timesteps: List[dict] = []
    
    for filepath in dir.glob("*.json"):
        with open(filepath) as f:
            jsondata: dict = json.load(f)

        timesteps.append(jsondata)

    return timesteps
