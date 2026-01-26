import os
import yaml
from pathlib import Path
from typing import Optional, Dict, Any

CONFIG_DIR = Path.home() / ".jolly"
CONFIG_FILE = CONFIG_DIR / "config.yaml"

class ConfigManager:
    """Manages configuration for jolly-flow CLI."""
    
    @staticmethod
    def _load_config() -> Dict[str, Any]:
        """Loads the configuration from the YAML file."""
        if not CONFIG_FILE.exists():
            return {}
        try:
            with open(CONFIG_FILE, "r") as f:
                return yaml.safe_load(f) or {}
        except Exception:
            return {}

    @staticmethod
    def _save_config(data: Dict[str, Any]) -> None:
        """Saves the configuration to the YAML file."""
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_FILE, "w") as f:
            yaml.dump(data, f)

    @staticmethod
    def set_key(key: str, value: str) -> None:
        """Sets a configuration key."""
        data = ConfigManager._load_config()
        data[key] = value
        ConfigManager._save_config(data)

    @staticmethod
    def get_key(key: str, default: Optional[str] = None) -> Optional[str]:
        """Retrieves a configuration key."""
        data = ConfigManager._load_config()
        return data.get(key, default)

    @staticmethod
    def get_vault_root() -> str:
        """Gets the configured vault root or default."""
        return ConfigManager.get_key("vault_root", str(Path.home() / "Documents/jolly-vault"))

    @staticmethod
    def get_projects_root() -> str:
        """Gets the configured projects root or default."""
        return ConfigManager.get_key("projects_root", str(Path.home() / "Documents/jolly-projects"))
