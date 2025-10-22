"""
Hybrid summarization combining extractive and abstractive methods.
"""

from typing import List, Dict, Any, Optional, Union
import logging
from ..extractive import TextRankSummarizer, BERTExtractiveSummarizer, LexRankSummarizer
from ..abstractive import T5Summarizer, BARTSummarizer, PegasusSummarizer
from ..utils.config_loader import ConfigLoader

logger = logging.getLogger(__name__)


class HybridSummarizer:
    """Hybrid summarization combining extractive and abstractive methods."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None, 
                 config_loader: Optional[ConfigLoader] = None):
        """
        Initialize hybrid summarizer.
        
        Args:
            config: Configuration dictionary
            config_loader: Configuration loader instance
        """
        self.config = config or {}
        self.config_loader = config_loader or ConfigLoader()
        self.extractive_summarizer = None
        self.abstractive_summarizer = None
        self.is_loaded = False
        
        # Load configuration
        self._load_configuration()
    
    def _load_configuration(self):
        """Load configuration for extractive and abstractive models."""
        # Get hybrid configuration
        hybrid_config = self.config_loader.get_hybrid_config()
        
        # Get weights
        self.extractive_weight = hybrid_config.get('weights', {}).get('extractive', 0.4)
        self.abstractive_weight = hybrid_config.get('weights', {}).get('abstractive', 0.6)
        
        # Get combination strategy
        self.combination_strategy = hybrid_config.get('combination_strategy', 'weighted_combination')
        
        # Initialize extractive summarizer
        self._initialize_extractive_summarizer()
        
        # Initialize abstractive summarizer
        self._initialize_abstractive_summarizer()
    
    def _initialize_extractive_summarizer(self):
        """Initialize extractive summarizer based on configuration."""
        extractive_config = self.config_loader.get_model_config('extractive', 'textrank')
        
        if extractive_config:
            self.extractive_summarizer = TextRankSummarizer(extractive_config)
        else:
            # Default configuration
            self.extractive_summarizer = TextRankSummarizer({
                'damping': 0.85,
                'max_iter': 100,
                'tol': 1e-6
            })
    
    def _initialize_abstractive_summarizer(self):
        """Initialize abstractive summarizer based on configuration."""
        abstractive_config = self.config_loader.get_model_config('abstractive', 't5')
        
        if abstractive_config:
            self.abstractive_summarizer = T5Summarizer(abstractive_config)
        else:
            # Default configuration
            self.abstractive_summarizer = T5Summarizer({
                'model_name': 't5-small',
                'max_length': 512,
                'min_length': 50,
                'num_beams': 4,
                'early_stopping': True
            })
    
    def load_models(self):
        """Load both extractive and abstractive models."""
        try:
            if self.extractive_summarizer:
                self.extractive_summarizer.load_model()
                logger.info("Extractive model loaded successfully")
            
            if self.abstractive_summarizer:
                self.abstractive_summarizer.load_model()
                logger.info("Abstractive model loaded successfully")
            
            self.is_loaded = True
            logger.info("All models loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading models: {str(e)}")
            raise
    
    def summarize(self, text: str, num_sentences: int = 5, 
                  max_length: int = 150, min_length: int = 30,
                  return_details: bool = False) -> Dict[str, Any]:
        """
        Generate hybrid summary combining extractive and abstractive methods.
        
        Args:
            text: Input text to summarize
            num_sentences: Number of sentences for extractive summarization
            max_length: Maximum length for abstractive summarization
            min_length: Minimum length for abstractive summarization
            return_details: Whether to return detailed information
            
        Returns:
            Dictionary containing hybrid summary and details
        """
        if not self.is_loaded:
            self.load_models()
        
        try:
            # Generate extractive summary
            extractive_result = None
            if self.extractive_summarizer:
                extractive_result = self.extractive_summarizer.summarize(
                    text, num_sentences, return_scores=True
                )
            
            # Generate abstractive summary
            abstractive_result = None
            if self.abstractive_summarizer:
                abstractive_result = self.abstractive_summarizer.summarize(
                    text, max_length, min_length, return_details=True
                )
            
            # Combine results based on strategy
            hybrid_summary = self._combine_summaries(
                extractive_result, abstractive_result, text
            )
            
            result = {
                'summary': hybrid_summary,
                'method': 'hybrid',
                'combination_strategy': self.combination_strategy,
                'extractive_weight': self.extractive_weight,
                'abstractive_weight': self.abstractive_weight
            }
            
            if return_details:
                result['details'] = {
                    'extractive_result': extractive_result,
                    'abstractive_result': abstractive_result,
                    'extractive_model': self.extractive_summarizer.__class__.__name__ if self.extractive_summarizer else None,
                    'abstractive_model': self.abstractive_summarizer.__class__.__name__ if self.abstractive_summarizer else None
                }
            
            return result
            
        except Exception as e:
            logger.error(f"Error during hybrid summarization: {str(e)}")
            raise
    
    def _combine_summaries(self, extractive_result: Optional[Dict[str, Any]], 
                          abstractive_result: Optional[Dict[str, Any]], 
                          original_text: str) -> str:
        """
        Combine extractive and abstractive summaries.
        
        Args:
            extractive_result: Result from extractive summarization
            abstractive_result: Result from abstractive summarization
            original_text: Original input text
            
        Returns:
            Combined summary
        """
        if self.combination_strategy == 'weighted_combination':
            return self._weighted_combination(extractive_result, abstractive_result)
        elif self.combination_strategy == 'pipeline':
            return self._pipeline_combination(extractive_result, abstractive_result)
        elif self.combination_strategy == 'ensemble':
            return self._ensemble_combination(extractive_result, abstractive_result)
        else:
            # Default to weighted combination
            return self._weighted_combination(extractive_result, abstractive_result)
    
    def _weighted_combination(self, extractive_result: Optional[Dict[str, Any]], 
                             abstractive_result: Optional[Dict[str, Any]]) -> str:
        """Combine summaries using weighted combination."""
        summaries = []
        
        if extractive_result and extractive_result.get('summary'):
            summaries.append(extractive_result['summary'])
        
        if abstractive_result and abstractive_result.get('summary'):
            summaries.append(abstractive_result['summary'])
        
        if not summaries:
            return "Unable to generate summary."
        
        # Simple concatenation for now
        # In a more sophisticated implementation, you could use more advanced combination methods
        return ' '.join(summaries)
    
    def _pipeline_combination(self, extractive_result: Optional[Dict[str, Any]], 
                             abstractive_result: Optional[Dict[str, Any]]) -> str:
        """Combine summaries using pipeline approach."""
        # Use extractive summary as input to abstractive model
        if extractive_result and extractive_result.get('summary'):
            extractive_text = extractive_result['summary']
            
            # Generate abstractive summary from extractive summary
            if self.abstractive_summarizer:
                try:
                    pipeline_result = self.abstractive_summarizer.summarize(
                        extractive_text, max_length=150, min_length=30
                    )
                    return pipeline_result['summary']
                except Exception as e:
                    logger.warning(f"Pipeline combination failed: {str(e)}")
                    return extractive_text
        
        # Fallback to abstractive only
        if abstractive_result and abstractive_result.get('summary'):
            return abstractive_result['summary']
        
        return "Unable to generate summary."
    
    def _ensemble_combination(self, extractive_result: Optional[Dict[str, Any]], 
                             abstractive_result: Optional[Dict[str, Any]]) -> str:
        """Combine summaries using ensemble approach."""
        summaries = []
        
        if extractive_result and extractive_result.get('summary'):
            summaries.append(extractive_result['summary'])
        
        if abstractive_result and abstractive_result.get('summary'):
            summaries.append(abstractive_result['summary'])
        
        if not summaries:
            return "Unable to generate summary."
        
        # For ensemble, we could implement more sophisticated combination methods
        # For now, use simple concatenation
        return ' '.join(summaries)
    
    def batch_summarize(self, texts: List[str], num_sentences: int = 5,
                       max_length: int = 150, min_length: int = 30) -> List[Dict[str, Any]]:
        """
        Summarize multiple texts using hybrid approach.
        
        Args:
            texts: List of texts to summarize
            num_sentences: Number of sentences for extractive summarization
            max_length: Maximum length for abstractive summarization
            min_length: Minimum length for abstractive summarization
            
        Returns:
            List of summarization results
        """
        results = []
        for text in texts:
            try:
                result = self.summarize(text, num_sentences, max_length, min_length)
                results.append(result)
            except Exception as e:
                logger.error(f"Error summarizing text: {str(e)}")
                results.append({
                    'summary': '',
                    'method': 'hybrid',
                    'error': str(e)
                })
        
        return results
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about loaded models."""
        info = {
            'is_loaded': self.is_loaded,
            'combination_strategy': self.combination_strategy,
            'extractive_weight': self.extractive_weight,
            'abstractive_weight': self.abstractive_weight
        }
        
        if self.extractive_summarizer:
            info['extractive_model'] = self.extractive_summarizer.get_model_info()
        
        if self.abstractive_summarizer:
            info['abstractive_model'] = self.abstractive_summarizer.get_model_info()
        
        return info