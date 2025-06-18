import yaml
import re


def load_config(path):
    """Load YAML config, stripping comments."""
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    # Remove comments
    content = re.sub(r'(?m)^\s*#.*\n?', '', content)
    return yaml.safe_load(content)
