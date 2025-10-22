"""
TextRank implementation for extractive text summarization.
"""

import numpy as np
from typing import List, Dict, Any, Optional
import logging
from collections import defaultdict
import networkx as nx
from .base import BaseExtractiveSummarizer
from ..utils.text_processing import TextProcessor

logger = logging.getLogger(__name__)


class TextRankSummarizer(BaseExtractiveSummarizer):
    """TextRank algorithm for extractive text summarization."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize TextRank summarizer.
        
        Args:
            config: Configuration dictionary
        """
        super().__init__(config)
        self.damping = self.config.get('damping', 0.85)
        self.max_iter = self.config.get('max_iter', 100)
        self.tol = self.config.get('tol', 1e-6)
        self.text_processor = TextProcessor()
    
    def load_model(self):
        """Load the TextRank model (no external model required)."""
        self.is_loaded = True
        logger.info("TextRank model loaded successfully")
    
    def _build_sentence_graph(self, sentences: List[str]) -> nx.Graph:
        """
        Build a graph where sentences are nodes and edges represent similarity.
        
        Args:
            sentences: List of sentences
            
        Returns:
            NetworkX graph
        """
        graph = nx.Graph()
        
        # Add nodes
        for i, sentence in enumerate(sentences):
            graph.add_node(i, sentence=sentence)
        
        # Add edges based on similarity
        for i in range(len(sentences)):
            for j in range(i + 1, len(sentences)):
                similarity = self._calculate_similarity(sentences[i], sentences[j])
                if similarity > 0:
                    graph.add_edge(i, j, weight=similarity)
        
        return graph
    
    def _calculate_similarity(self, sent1: str, sent2: str) -> float:
        """
        Calculate similarity between two sentences.
        
        Args:
            sent1: First sentence
            sent2: Second sentence
            
        Returns:
            Similarity score between 0 and 1
        """
        # Tokenize sentences
        words1 = set(self.text_processor.tokenize_words(sent1))
        words2 = set(self.text_processor.tokenize_words(sent2))
        
        if not words1 or not words2:
            return 0.0
        
        # Calculate Jaccard similarity
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union if union > 0 else 0.0
    
    def _calculate_textrank_scores(self, graph: nx.Graph) -> Dict[int, float]:
        """
        Calculate TextRank scores for sentences.
        
        Args:
            graph: Sentence similarity graph
            
        Returns:
            Dictionary mapping sentence indices to scores
        """
        # Initialize scores
        scores = {node: 1.0 for node in graph.nodes()}
        
        # Iterative calculation
        for _ in range(self.max_iter):
            prev_scores = scores.copy()
            
            for node in graph.nodes():
                score = 0.0
                for neighbor in graph.neighbors(node):
                    edge_weight = graph[node][neighbor]['weight']
                    neighbor_score = prev_scores[neighbor]
                    neighbor_degree = graph.degree(neighbor)
                    
                    if neighbor_degree > 0:
                        score += edge_weight * neighbor_score / neighbor_degree
                
                scores[node] = (1 - self.damping) + self.damping * score
            
            # Check convergence
            if all(abs(scores[node] - prev_scores[node]) < self.tol for node in scores):
                break
        
        return scores
    
    def extract_sentences(self, text: str, num_sentences: int = 5) -> List[str]:
        """
        Extract the most important sentences using TextRank.
        
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
        
        # Build sentence graph
        graph = self._build_sentence_graph(sentences)
        
        if len(graph.nodes()) == 0:
            return sentences[:num_sentences]
        
        # Calculate TextRank scores
        scores = self._calculate_textrank_scores(graph)
        
        # Sort sentences by score
        sorted_sentences = sorted(
            [(i, sentences[i], scores[i]) for i in range(len(sentences))],
            key=lambda x: x[2],
            reverse=True
        )
        
        # Select top sentences
        selected_sentences = [sent[1] for sent in sorted_sentences[:num_sentences]]
        
        # Sort selected sentences by original order
        selected_sentences.sort(key=lambda x: sentences.index(x))
        
        return selected_sentences
    
    def _get_sentence_scores(self, text: str, sentences: List[str]) -> Dict[str, float]:
        """
        Get TextRank scores for sentences.
        
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
        
        # Build sentence graph
        graph = self._build_sentence_graph(all_sentences)
        
        if len(graph.nodes()) == 0:
            return {sentence: 1.0 for sentence in sentences}
        
        # Calculate TextRank scores
        scores = self._calculate_textrank_scores(graph)
        
        # Map sentences to scores
        sentence_scores = {}
        for i, sentence in enumerate(all_sentences):
            if sentence in sentences:
                sentence_scores[sentence] = scores.get(i, 0.0)
        
        return sentence_scores
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get TextRank model information."""
        info = super().get_model_info()
        info.update({
            'damping': self.damping,
            'max_iter': self.max_iter,
            'tolerance': self.tol
        })
        return info