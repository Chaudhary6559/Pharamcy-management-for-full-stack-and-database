"""
T5-based abstractive text summarization.
"""

import torch
from typing import List, Dict, Any, Optional
import logging
from transformers import T5ForConditionalGeneration, T5Tokenizer
from .base import BaseAbstractiveSummarizer

logger = logging.getLogger(__name__)


class T5Summarizer(BaseAbstractiveSummarizer):
    """T5 model for abstractive text summarization."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize T5 summarizer.
        
        Args:
            config: Configuration dictionary
        """
        super().__init__(config)
        self.model_name = self.config.get('model_name', 't5-small')
        self.max_length = self.config.get('max_length', 512)
        self.min_length = self.config.get('min_length', 50)
        self.num_beams = self.config.get('num_beams', 4)
        self.early_stopping = self.config.get('early_stopping', True)
        self.temperature = self.config.get('temperature', 1.0)
        self.do_sample = self.config.get('do_sample', False)
        self.top_p = self.config.get('top_p', 1.0)
        self.top_k = self.config.get('top_k', 50)
        self.repetition_penalty = self.config.get('repetition_penalty', 1.0)
    
    def load_model(self):
        """Load T5 model and tokenizer."""
        try:
            # Load tokenizer
            self.tokenizer = T5Tokenizer.from_pretrained(self.model_name)
            
            # Load model
            self.model = T5ForConditionalGeneration.from_pretrained(self.model_name)
            
            # Move to device
            if torch.cuda.is_available() and self.device != 'cpu':
                self.device = 'cuda'
                self.model = self.model.to(self.device)
            else:
                self.device = 'cpu'
            
            self.is_loaded = True
            logger.info(f"T5 model {self.model_name} loaded successfully on {self.device}")
            
        except Exception as e:
            logger.error(f"Error loading T5 model: {str(e)}")
            raise
    
    def _preprocess_text(self, text: str) -> str:
        """
        Preprocess text for T5 summarization.
        
        Args:
            text: Input text
            
        Returns:
            Preprocessed text
        """
        # T5 expects "summarize: " prefix for summarization
        if not text.startswith("summarize: "):
            text = f"summarize: {text}"
        
        return text
    
    def generate_summary(self, text: str, max_length: int = 150, 
                        min_length: int = 30) -> str:
        """
        Generate summary using T5 model.
        
        Args:
            text: Input text to summarize
            max_length: Maximum length of summary
            min_length: Minimum length of summary
            
        Returns:
            Generated summary
        """
        if not self.is_loaded:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        # Preprocess text
        processed_text = self._preprocess_text(text)
        
        # Tokenize input
        inputs = self.tokenizer(
            processed_text,
            max_length=self.max_length,
            padding=True,
            truncation=True,
            return_tensors="pt"
        )
        
        # Move to device
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        # Generate summary
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                min_length=min_length,
                num_beams=self.num_beams,
                early_stopping=self.early_stopping,
                temperature=self.temperature,
                do_sample=self.do_sample,
                top_p=self.top_p,
                top_k=self.top_k,
                repetition_penalty=self.repetition_penalty,
                pad_token_id=self.tokenizer.pad_token_id,
                eos_token_id=self.tokenizer.eos_token_id
            )
        
        # Decode output
        summary = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        return summary
    
    def _get_generation_details(self, text: str, summary: str) -> Dict[str, Any]:
        """Get T5-specific generation details."""
        details = super()._get_generation_details(text, summary)
        details.update({
            'model_name': self.model_name,
            'num_beams': self.num_beams,
            'early_stopping': self.early_stopping,
            'temperature': self.temperature,
            'do_sample': self.do_sample,
            'top_p': self.top_p,
            'top_k': self.top_k,
            'repetition_penalty': self.repetition_penalty
        })
        return details
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get T5 model information."""
        info = super().get_model_info()
        info.update({
            'model_name': self.model_name,
            'max_length': self.max_length,
            'min_length': self.min_length,
            'num_beams': self.num_beams,
            'early_stopping': self.early_stopping,
            'temperature': self.temperature,
            'do_sample': self.do_sample
        })
        return info