"""
Base class for abstractive summarization methods.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class BaseAbstractiveSummarizer(ABC):
    """Base class for all abstractive summarization methods."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the abstractive summarizer.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.model = None
        self.tokenizer = None
        self.is_loaded = False
        self.device = self.config.get('device', 'cpu')
    
    @abstractmethod
    def load_model(self):
        """Load the required model and tokenizer for summarization."""
        pass
    
    @abstractmethod
    def generate_summary(self, text: str, max_length: int = 150, 
                        min_length: int = 30) -> str:
        """
        Generate abstractive summary from text.
        
        Args:
            text: Input text to summarize
            max_length: Maximum length of summary
            min_length: Minimum length of summary
            
        Returns:
            Generated summary
        """
        pass
    
    def summarize(self, text: str, max_length: int = 150, 
                  min_length: int = 30, return_details: bool = False) -> Dict[str, Any]:
        """
        Summarize text using abstractive methods.
        
        Args:
            text: Input text to summarize
            max_length: Maximum length of summary
            min_length: Minimum length of summary
            return_details: Whether to return generation details
            
        Returns:
            Dictionary containing summary and optional details
        """
        if not self.is_loaded:
            self.load_model()
        
        try:
            summary = self.generate_summary(text, max_length, min_length)
            
            result = {
                'summary': summary,
                'method': self.__class__.__name__,
                'max_length': max_length,
                'min_length': min_length
            }
            
            if return_details:
                result['details'] = self._get_generation_details(text, summary)
            
            return result
            
        except Exception as e:
            logger.error(f"Error during summarization: {str(e)}")
            raise
    
    def _get_generation_details(self, text: str, summary: str) -> Dict[str, Any]:
        """
        Get additional details about the generation process.
        
        Args:
            text: Original text
            summary: Generated summary
            
        Returns:
            Dictionary containing generation details
        """
        return {
            'input_length': len(text),
            'output_length': len(summary),
            'compression_ratio': len(summary) / len(text) if len(text) > 0 else 0,
            'model_name': self.config.get('model_name', 'unknown')
        }
    
    def batch_summarize(self, texts: List[str], max_length: int = 150, 
                       min_length: int = 30) -> List[Dict[str, Any]]:
        """
        Summarize multiple texts in batch.
        
        Args:
            texts: List of texts to summarize
            max_length: Maximum length of summary
            min_length: Minimum length of summary
            
        Returns:
            List of summarization results
        """
        results = []
        for text in texts:
            try:
                result = self.summarize(text, max_length, min_length)
                results.append(result)
            except Exception as e:
                logger.error(f"Error summarizing text: {str(e)}")
                results.append({
                    'summary': '',
                    'method': self.__class__.__name__,
                    'max_length': max_length,
                    'min_length': min_length,
                    'error': str(e)
                })
        
        return results
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the loaded model.
        
        Returns:
            Dictionary containing model information
        """
        return {
            'class': self.__class__.__name__,
            'is_loaded': self.is_loaded,
            'device': self.device,
            'config': self.config
        }