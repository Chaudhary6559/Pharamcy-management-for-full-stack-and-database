"""
Base class for extractive summarization methods.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class BaseExtractiveSummarizer(ABC):
    """Base class for all extractive summarization methods."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the extractive summarizer.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.model = None
        self.is_loaded = False
    
    @abstractmethod
    def load_model(self):
        """Load the required model for summarization."""
        pass
    
    @abstractmethod
    def extract_sentences(self, text: str, num_sentences: int = 5) -> List[str]:
        """
        Extract the most important sentences from the text.
        
        Args:
            text: Input text to summarize
            num_sentences: Number of sentences to extract
            
        Returns:
            List of extracted sentences
        """
        pass
    
    def summarize(self, text: str, num_sentences: int = 5, 
                  return_scores: bool = False) -> Dict[str, Any]:
        """
        Summarize text using extractive methods.
        
        Args:
            text: Input text to summarize
            num_sentences: Number of sentences to extract
            return_scores: Whether to return sentence scores
            
        Returns:
            Dictionary containing summary and optional scores
        """
        if not self.is_loaded:
            self.load_model()
        
        try:
            sentences = self.extract_sentences(text, num_sentences)
            
            result = {
                'summary': ' '.join(sentences),
                'sentences': sentences,
                'num_sentences': len(sentences),
                'method': self.__class__.__name__
            }
            
            if return_scores:
                result['scores'] = self._get_sentence_scores(text, sentences)
            
            return result
            
        except Exception as e:
            logger.error(f"Error during summarization: {str(e)}")
            raise
    
    def _get_sentence_scores(self, text: str, sentences: List[str]) -> Dict[str, float]:
        """
        Get scores for extracted sentences.
        
        Args:
            text: Original text
            sentences: Extracted sentences
            
        Returns:
            Dictionary mapping sentences to their scores
        """
        # Default implementation - can be overridden by subclasses
        return {sentence: 1.0 for sentence in sentences}
    
    def batch_summarize(self, texts: List[str], num_sentences: int = 5) -> List[Dict[str, Any]]:
        """
        Summarize multiple texts in batch.
        
        Args:
            texts: List of texts to summarize
            num_sentences: Number of sentences to extract per text
            
        Returns:
            List of summarization results
        """
        results = []
        for text in texts:
            try:
                result = self.summarize(text, num_sentences)
                results.append(result)
            except Exception as e:
                logger.error(f"Error summarizing text: {str(e)}")
                results.append({
                    'summary': '',
                    'sentences': [],
                    'num_sentences': 0,
                    'method': self.__class__.__name__,
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
            'config': self.config
        }