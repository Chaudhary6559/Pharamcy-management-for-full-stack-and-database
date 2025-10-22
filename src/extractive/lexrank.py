"""
LexRank implementation for extractive text summarization.
"""

import numpy as np
from typing import List, Dict, Any, Optional
import logging
from collections import defaultdict
from .base import BaseExtractiveSummarizer
from ..utils.text_processing import TextProcessor

logger = logging.getLogger(__name__)


class LexRankSummarizer(BaseExtractiveSummarizer):
    """LexRank algorithm for extractive text summarization."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize LexRank summarizer.
        
        Args:
            config: Configuration dictionary
        """
        super().__init__(config)
        self.threshold = self.config.get('threshold', 0.1)
        self.max_sentences = self.config.get('max_sentences', 5)
        self.text_processor = TextProcessor()
    
    def load_model(self):
        """Load the LexRank model (no external model required)."""
        self.is_loaded = True
        logger.info("LexRank model loaded successfully")
    
    def _build_similarity_matrix(self, sentences: List[str]) -> np.ndarray:
        """
        Build similarity matrix between sentences.
        
        Args:
            sentences: List of sentences
            
        Returns:
            Similarity matrix
        """
        n = len(sentences)
        similarity_matrix = np.zeros((n, n))
        
        for i in range(n):
            for j in range(n):
                if i != j:
                    similarity = self._calculate_similarity(sentences[i], sentences[j])
                    similarity_matrix[i][j] = similarity
        
        return similarity_matrix
    
    def _calculate_similarity(self, sent1: str, sent2: str) -> float:
        """
        Calculate cosine similarity between two sentences.
        
        Args:
            sent1: First sentence
            sent2: Second sentence
            
        Returns:
            Similarity score between 0 and 1
        """
        # Tokenize and get word frequencies
        words1 = self.text_processor.tokenize_words(sent1, remove_stopwords=True)
        words2 = self.text_processor.tokenize_words(sent2, remove_stopwords=True)
        
        if not words1 or not words2:
            return 0.0
        
        # Create word frequency vectors
        all_words = set(words1 + words2)
        vec1 = np.array([words1.count(word) for word in all_words])
        vec2 = np.array([words2.count(word) for word in all_words])
        
        # Calculate cosine similarity
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        similarity = dot_product / (norm1 * norm2)
        return similarity
    
    def _build_lexrank_matrix(self, similarity_matrix: np.ndarray) -> np.ndarray:
        """
        Build LexRank transition matrix.
        
        Args:
            similarity_matrix: Sentence similarity matrix
            
        Returns:
            LexRank transition matrix
        """
        n = similarity_matrix.shape[0]
        
        # Create adjacency matrix based on threshold
        adjacency_matrix = (similarity_matrix >= self.threshold).astype(float)
        
        # Remove self-loops
        np.fill_diagonal(adjacency_matrix, 0)
        
        # Calculate row sums
        row_sums = np.sum(adjacency_matrix, axis=1)
        
        # Create transition matrix
        transition_matrix = np.zeros((n, n))
        for i in range(n):
            if row_sums[i] > 0:
                transition_matrix[i] = adjacency_matrix[i] / row_sums[i]
            else:
                # Handle isolated nodes
                transition_matrix[i] = np.ones(n) / n
        
        return transition_matrix
    
    def _calculate_lexrank_scores(self, transition_matrix: np.ndarray, 
                                 damping: float = 0.85, 
                                 max_iter: int = 100,
                                 tol: float = 1e-6) -> np.ndarray:
        """
        Calculate LexRank scores using power iteration.
        
        Args:
            transition_matrix: LexRank transition matrix
            damping: Damping factor
            max_iter: Maximum iterations
            tol: Convergence tolerance
            
        Returns:
            LexRank scores
        """
        n = transition_matrix.shape[0]
        
        # Initialize scores
        scores = np.ones(n) / n
        
        # Power iteration
        for _ in range(max_iter):
            prev_scores = scores.copy()
            
            # Update scores
            scores = (1 - damping) / n + damping * np.dot(transition_matrix.T, scores)
            
            # Check convergence
            if np.allclose(scores, prev_scores, atol=tol):
                break
        
        return scores
    
    def extract_sentences(self, text: str, num_sentences: int = 5) -> List[str]:
        """
        Extract the most important sentences using LexRank.
        
        Args:
            text: Input text to summarize
            num_sentences: Number of sentences to extract
            
        Returns:
            List of extracted sentences
        """
        # Preprocess text
        sentences = self.text_processor.preprocess_for_summarization(text)
        
        if len(sentences) <= num_sentences:
            return sentences
        
        # Build similarity matrix
        similarity_matrix = self._build_similarity_matrix(sentences)
        
        # Build LexRank transition matrix
        transition_matrix = self._build_lexrank_matrix(similarity_matrix)
        
        # Calculate LexRank scores
        scores = self._calculate_lexrank_scores(transition_matrix)
        
        # Select top sentences
        top_indices = np.argsort(scores)[-num_sentences:]
        top_indices = sorted(top_indices)  # Sort by original order
        
        selected_sentences = [sentences[i] for i in top_indices]
        
        return selected_sentences
    
    def _get_sentence_scores(self, text: str, sentences: List[str]) -> Dict[str, float]:
        """
        Get LexRank scores for sentences.
        
        Args:
            text: Original text
            sentences: Extracted sentences
            
        Returns:
            Dictionary mapping sentences to their scores
        """
        # Preprocess text
        all_sentences = self.text_processor.preprocess_for_summarization(text)
        
        if len(all_sentences) <= len(sentences):
            return {sentence: 1.0 for sentence in sentences}
        
        # Build similarity matrix
        similarity_matrix = self._build_similarity_matrix(all_sentences)
        
        # Build LexRank transition matrix
        transition_matrix = self._build_lexrank_matrix(similarity_matrix)
        
        # Calculate LexRank scores
        scores = self._calculate_lexrank_scores(transition_matrix)
        
        # Normalize scores
        max_score = np.max(scores)
        normalized_scores = scores / max_score if max_score > 0 else scores
        
        # Map sentences to scores
        sentence_scores = {}
        for i, sentence in enumerate(all_sentences):
            if sentence in sentences:
                sentence_scores[sentence] = float(normalized_scores[i])
        
        return sentence_scores
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get LexRank model information."""
        info = super().get_model_info()
        info.update({
            'threshold': self.threshold,
            'max_sentences': self.max_sentences
        })
        return info