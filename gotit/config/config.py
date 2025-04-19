import os
import logging
import yaml
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('/app/logs/app.log')
    ]
)

def load_config():
    """
    Load configuration from YAML file or environment variables.
    Environment variables take precedence over YAML config.
    
    Returns:
        dict: Configuration dictionary with API keys and settings
    """
    config = {
        'slack': {'bot_token': os.getenv('SLACK_BOT_TOKEN')},
        'notion': {'api_key': os.getenv('NOTION_API_KEY')},
        'gemini': {'api_key': os.getenv('GEMINI_API_KEY')}
    }

    # Try to load from YAML file if it exists
    try:
        config_dir = Path(__file__).parent
        config_path = config_dir / "config.yaml"
        
        if config_path.exists():
            with open(config_path, 'r') as f:
                yaml_config = yaml.safe_load(f)
                
            # Update config with YAML values, but don't override environment variables
            for section in ['slack', 'notion', 'gemini']:
                if section in yaml_config:
                    for key, value in yaml_config[section].items():
                        if not config[section].get(key):  # Only use YAML value if env var not set
                            config[section][key] = value
    except Exception as e:
        logging.warning(f"Could not load YAML config: {e}")
    
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
            if not config[section].get(key):
                missing_keys.append(f"'{section}.{key}'")
    
    if missing_keys:
        raise ValueError(f"Missing required configuration keys: {', '.join(missing_keys)}")
    
    logging.info("Successfully loaded configuration")
    return config 