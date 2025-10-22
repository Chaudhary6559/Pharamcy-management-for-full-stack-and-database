"""
BERT-based extractive summarization using sentence embeddings and similarity.
"""

import numpy as np
from typing import List, Dict, Any, Optional, Tuple
import logging
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from .base import BaseExtractiveSummarizer
from ..utils.text_processing import TextProcessor

logger = logging.getLogger(__name__)


class BERTExtractiveSummarizer(BaseExtractiveSummarizer):
    """BERT-based extractive summarization using sentence embeddings."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize BERT extractive summarizer.
        
        Args:
            config: Configuration dictionary
        """
        super().__init__(config)
        self.model_name = self.config.get('model_name', 'sentence-transformers/all-MiniLM-L6-v2')
        self.similarity_threshold = self.config.get('similarity_threshold', 0.7)
        self.max_sentences = self.config.get('max_sentences', 5)
        self.text_processor = TextProcessor()
        self.sentence_model = None
    
    def load_model(self):
        """Load the BERT sentence transformer model."""
        try:
            self.sentence_model = SentenceTransformer(self.model_name)
            self.is_loaded = True
            logger.info(f"BERT model {self.model_name} loaded successfully")
        except Exception as e:
            logger.error(f"Error loading BERT model: {str(e)}")
            raise
    
    def _get_sentence_embeddings(self, sentences: List[str]) -> np.ndarray:
        """
        Get sentence embeddings using BERT.
        
        Args:
            sentences: List of sentences
            
        Returns:
            Array of sentence embeddings
        """
        if not self.is_loaded:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        embeddings = self.sentence_model.encode(sentences)
        return embeddings
    
    def _calculate_sentence_similarities(self, embeddings: np.ndarray) -> np.ndarray:
        """
        Calculate pairwise similarities between sentences.
        
        Args:
            embeddings: Sentence embeddings
            
        Returns:
            Similarity matrix
        """
        similarities = cosine_similarity(embeddings)
        return similarities
    
    def _select_diverse_sentences(self, sentences: List[str], 
                                 embeddings: np.ndarray, 
                                 num_sentences: int) -> List[str]:
        """
        Select diverse sentences using MMR (Maximal Marginal Relevance).
        
        Args:
            sentences: List of sentences
            embeddings: Sentence embeddings
            num_sentences: Number of sentences to select
            
        Returns:
            List of selected sentences
        """
        if len(sentences) <= num_sentences:
            return sentences
        
        # Calculate similarities
        similarities = self._calculate_sentence_similarities(embeddings)
        
        # Calculate sentence importance (average similarity to all other sentences)
        importance_scores = np.mean(similarities, axis=1)
        
        # MMR selection
        selected_indices = []
        remaining_indices = list(range(len(sentences)))
        
        # Select first sentence with highest importance
        first_idx = np.argmax(importance_scores)
        selected_indices.append(first_idx)
        remaining_indices.remove(first_idx)
        
        # Select remaining sentences using MMR
        for _ in range(min(num_sentences - 1, len(remaining_indices))):
            best_idx = None
            best_score = -1
            
            for idx in remaining_indices:
                # Calculate MMR score
                relevance = importance_scores[idx]
                max_similarity = max(similarities[idx][sel_idx] for sel_idx in selected_indices)
                mmr_score = relevance - (0.5 * max_similarity)  # Lambda = 0.5
                
                if mmr_score > best_score:
                    best_score = mmr_score
                    best_idx = idx
            
            if best_idx is not None:
                selected_indices.append(best_idx)
                remaining_indices.remove(best_idx)
        
        # Sort by original order
        selected_indices.sort()
        return [sentences[i] for i in selected_indices]
    
    def _select_important_sentences(self, sentences: List[str], 
                                   embeddings: np.ndarray, 
                                   num_sentences: int) -> List[str]:
        """
        Select most important sentences based on centrality.
        
        Args:
            sentences: List of sentences
            embeddings: Sentence embeddings
            num_sentences: Number of sentences to select
            
        Returns:
            List of selected sentences
        """
        if len(sentences) <= num_sentences:
            return sentences
        
        # Calculate similarities
        similarities = self._calculate_sentence_similarities(embeddings)
        
        # Calculate centrality scores (sum of similarities to all other sentences)
        centrality_scores = np.sum(similarities, axis=1)
        
        # Select top sentences
        top_indices = np.argsort(centrality_scores)[-num_sentences:]
        top_indices = sorted(top_indices)  # Sort by original order
        
        return [sentences[i] for i in top_indices]
    
    def extract_sentences(self, text: str, num_sentences: int = 5) -> List[str]:
        """
        Extract the most important sentences using BERT embeddings.
        
        Args:
            text: Input text to summarize
            num_sentences: Number of sentences to extract
            
        Returns:
            List of extracted sentences
        """
        if not self.is_loaded:
            self.load_model()
        
        # Preprocess text
        sentences = self.text_processor.preprocess_for_summarization(text)
        
        if len(sentences) <= num_sentences:
            return sentences
        
        # Get sentence embeddings
        embeddings = self._get_sentence_embeddings(sentences)
        
        # Select sentences using diversity-based approach
        selected_sentences = self._select_diverse_sentences(sentences, embeddings, num_sentences)
        
        return selected_sentences
    
    def _get_sentence_scores(self, text: str, sentences: List[str]) -> Dict[str, float]:
        """
        Get BERT-based scores for sentences.
        
        Args:
            text: Original text
            sentences: Extracted sentences
            
        Returns:
            Dictionary mapping sentences to their scores
        """
        if not self.is_loaded:
            self.load_model()
        
        # Preprocess text
        all_sentences = self.text_processor.preprocess_for_summarization(text)
        
        if len(all_sentences) <= len(sentences):
            return {sentence: 1.0 for sentence in sentences}
        
        # Get sentence embeddings
        embeddings = self._get_sentence_embeddings(all_sentences)
        
        # Calculate centrality scores
        similarities = self._calculate_sentence_similarities(embeddings)
        centrality_scores = np.sum(similarities, axis=1)
        
        # Normalize scores
        max_score = np.max(centrality_scores)
        normalized_scores = centrality_scores / max_score if max_score > 0 else centrality_scores
        
        # Map sentences to scores
        sentence_scores = {}
        for i, sentence in enumerate(all_sentences):
            if sentence in sentences:
                sentence_scores[sentence] = float(normalized_scores[i])
        
        return sentence_scores
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get BERT model information."""
        info = super().get_model_info()
        info.update({
            'model_name': self.model_name,
            'similarity_threshold': self.similarity_threshold,
            'max_sentences': self.max_sentences
        })
        return info