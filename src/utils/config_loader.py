"""
Configuration loader for managing project settings and parameters.
"""

import yaml
import os
from typing import Dict, Any, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class ConfigLoader:
    """Configuration loader for managing project settings."""
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize the configuration loader.
        
        Args:
            config_path: Path to the configuration file
        """
        self.config_path = Path(config_path)
        self.config = {}
        self._load_config()
    
    def _load_config(self):
        """Load configuration from file."""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self.config = yaml.safe_load(f)
                logger.info(f"Configuration loaded from {self.config_path}")
            except Exception as e:
                logger.error(f"Error loading configuration: {str(e)}")
                self.config = self._get_default_config()
        else:
            logger.warning(f"Configuration file {self.config_path} not found, using defaults")
            self.config = self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            'models': {
                'extractive': {
                    'textrank': {
                        'damping': 0.85,
                        'max_iter': 100,
                        'tol': 1e-6
                    },
                    'bert_extractive': {
                        'model_name': 'sentence-transformers/all-MiniLM-L6-v2',
                        'similarity_threshold': 0.7,
                        'max_sentences': 5
                    }
                },
                'abstractive': {
                    't5': {
                        'model_name': 't5-small',
                        'max_length': 512,
                        'min_length': 50,
                        'num_beams': 4,
                        'early_stopping': True
                    }
                }
            },
            'hybrid': {
                'weights': {
                    'extractive': 0.4,
                    'abstractive': 0.6
                }
            },
            'evaluation': {
                'metrics': ['rouge-1', 'rouge-2', 'rouge-l', 'bleu', 'bert_score']
            },
            'data': {
                'max_input_length': 2048,
                'min_sentence_length': 10,
                'max_sentence_length': 200,
                'language': 'en'
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value using dot notation.
        
        Args:
            key: Configuration key (e.g., 'models.extractive.textrank.damping')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any):
        """
        Set a configuration value using dot notation.
        
        Args:
            key: Configuration key
            value: Value to set
        """
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def save_config(self, file_path: Optional[str] = None):
        """
        Save configuration to file.
        
        Args:
            file_path: Optional custom file path
        """
        save_path = Path(file_path) if file_path else self.config_path
        save_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(save_path, 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f, default_flow_style=False, indent=2)
            logger.info(f"Configuration saved to {save_path}")
        except Exception as e:
            logger.error(f"Error saving configuration: {str(e)}")
    
    def get_model_config(self, model_type: str, model_name: str) -> Dict[str, Any]:
        """
        Get configuration for a specific model.
        
        Args:
            model_type: Type of model (extractive, abstractive)
            model_name: Name of the model
            
        Returns:
            Model configuration
        """
        return self.get(f'models.{model_type}.{model_name}', {})
    
    def get_evaluation_config(self) -> Dict[str, Any]:
        """Get evaluation configuration."""
        return self.get('evaluation', {})
    
    def get_data_config(self) -> Dict[str, Any]:
        """Get data processing configuration."""
        return self.get('data', {})
    
    def get_hybrid_config(self) -> Dict[str, Any]:
        """Get hybrid summarization configuration."""
        return self.get('hybrid', {})
    
    def update_from_env(self):
        """Update configuration from environment variables."""
        env_mappings = {
            'MODEL_DEVICE': 'device',
            'MAX_INPUT_LENGTH': 'data.max_input_length',
            'BATCH_SIZE': 'training.batch_size',
            'LEARNING_RATE': 'training.learning_rate',
            'NUM_EPOCHS': 'training.num_epochs',
            'LOG_LEVEL': 'logging.level',
            'USE_WANDB': 'logging.use_wandb',
            'WANDB_PROJECT': 'logging.wandb_project'
        }
        
        for env_var, config_key in env_mappings.items():
            value = os.getenv(env_var)
            if value is not None:
                # Convert string values to appropriate types
                if value.lower() in ['true', 'false']:
                    value = value.lower() == 'true'
                elif value.isdigit():
                    value = int(value)
                elif '.' in value and value.replace('.', '').isdigit():
                    value = float(value)
                
                self.set(config_key, value)
                logger.info(f"Updated {config_key} from environment: {value}")
    
    def validate_config(self) -> bool:
        """
        Validate the configuration.
        
        Returns:
            True if configuration is valid, False otherwise
        """
        required_keys = [
            'models.extractive',
            'models.abstractive',
            'evaluation.metrics',
            'data.max_input_length'
        ]
        
        for key in required_keys:
            if self.get(key) is None:
                logger.error(f"Missing required configuration key: {key}")
                return False
        
        # Validate model configurations
        extractive_models = self.get('models.extractive', {})
        abstractive_models = self.get('models.abstractive', {})
        
        if not extractive_models and not abstractive_models:
            logger.error("At least one extractive or abstractive model must be configured")
            return False
        
        return True