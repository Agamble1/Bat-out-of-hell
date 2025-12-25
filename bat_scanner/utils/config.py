"""
Configuration management for BAT Scanner.
"""
import json
import yaml
from pathlib import Path
from typing import Dict, Any


class Config:
    """Configuration manager for BAT Scanner."""
    
    def __init__(self, config_file: str = None):
        """
        Initialize configuration.
        
        Args:
            config_file: Path to configuration file (JSON or YAML)
        """
        self.config = self._load_default_config()
        
        if config_file:
            self.load_from_file(config_file)
            
    def _load_default_config(self) -> Dict[str, Any]:
        """
        Load default configuration.
        
        Returns:
            Default configuration dictionary
        """
        return {
            "scanner": {
                "timeout": 5,
                "max_threads": 10,
                "user_agent": "BAT-Scanner/1.0"
            },
            "port_scanner": {
                "timeout": 1,
                "ports": [21, 22, 23, 25, 80, 443, 3306, 3389, 8080, 8443]
            },
            "logging": {
                "level": "INFO",
                "file": "logs/bat_scanner.log"
            },
            "reports": {
                "output_dir": "reports",
                "format": "json"
            }
        }
        
    def load_from_file(self, config_file: str):
        """
        Load configuration from file.
        
        Args:
            config_file: Path to configuration file
        """
        file_path = Path(config_file)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_file}")
            
        with open(file_path, 'r') as f:
            if file_path.suffix == '.json':
                loaded_config = json.load(f)
            elif file_path.suffix in ['.yml', '.yaml']:
                loaded_config = yaml.safe_load(f)
            else:
                raise ValueError(f"Unsupported configuration file format: {file_path.suffix}")
                
        self.config.update(loaded_config)
        
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.
        
        Args:
            key: Configuration key (supports dot notation, e.g., 'scanner.timeout')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
                
        return value
        
    def set(self, key: str, value: Any):
        """
        Set configuration value.
        
        Args:
            key: Configuration key (supports dot notation)
            value: Value to set
        """
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
            
        config[keys[-1]] = value
        
    def save_to_file(self, config_file: str):
        """
        Save configuration to file.
        
        Args:
            config_file: Path to save configuration
        """
        file_path = Path(config_file)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w') as f:
            if file_path.suffix == '.json':
                json.dump(self.config, f, indent=2)
            elif file_path.suffix in ['.yml', '.yaml']:
                yaml.dump(self.config, f, default_flow_style=False)
            else:
                raise ValueError(f"Unsupported configuration file format: {file_path.suffix}")
