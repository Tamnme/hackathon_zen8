import os
import logging
import yaml
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_config():
    """
    Load configuration from YAML file.
    
    Returns:
        dict: Configuration dictionary with API keys and settings
    """
    try:
        # Get the directory where this script is located
        config_dir = Path(__file__).parent
        config_path = config_dir / "config.yaml"
        
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found at {config_path}")
        
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            
        # Validate required configuration
        required_keys = {
            'slack': ['bot_token'],
            'notion': ['api_key'],
            'gemini': ['api_key']
        }
        
        missing_keys = []
        for section, keys in required_keys.items():
            if section not in config:
                missing_keys.append(f"Section '{section}'")
                continue
            for key in keys:
                if key not in config[section]:
                    missing_keys.append(f"'{section}.{key}'")
        
        if missing_keys:
            raise ValueError(f"Missing required configuration keys: {', '.join(missing_keys)}")
        
        logging.info("Successfully loaded configuration from YAML file.")
        return config
        
    except yaml.YAMLError as e:
        logging.error(f"Error parsing YAML configuration: {e}")
        raise
    except Exception as e:
        logging.error(f"Error loading configuration: {e}")
        raise 