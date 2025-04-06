import yaml
from pathlib import Path

def load_config():
    """
    load the configuration file
    """

    config_path = Path(__file__).parent.parent.parent / "config.yaml"
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
        return config