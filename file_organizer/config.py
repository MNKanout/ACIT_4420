# config.py

import json
import os

def load_config(config_path='config.json'):
    if not os.path.exists(config_path):
        # Return default configuration
        return {}
    with open(config_path, 'r') as f:
        config = json.load(f)
    return config
