import json
import os

def load_master_data():
    """Loads the Master CV JSON from the data directory."""
    # Build path relative to this file
    base_path = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(base_path, 'data', 'master_cv.json')
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

print(load_master_data())
print(type(load_master_data()))