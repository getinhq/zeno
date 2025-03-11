import os
from pathlib import Path

def load_env_file():
    env_path = Path(__file__).parent / '.env'
    if not env_path.exists():
        return
    
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.replace('"', '').split('=', 1)
                os.environ[key.strip()] = value.strip()