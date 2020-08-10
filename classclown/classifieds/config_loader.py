from types import resolve_bases
from typing import Dict, Text


from typing import Text, Dict
import json
import os


def load_config(location: Text) -> Dict:
    resolved_path = os.path.join(os.getcwd(), location)
    print(resolved_path)
    with open(resolved_path) as config_file:
        config = json.load(config_file)
        print(config)
        return config
