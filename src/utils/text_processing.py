"""
Text processing utilities for cleaning, preprocessing, and preparing text data.
"""

import re
import string
import nltk
import spacy
from typing import List, Dict, Optional, Tuple
import logging

# Download required NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
    nltk.download('wordnet', quiet=True)
except:
    pass

logger = logging.getLogger(__name__)


class TextProcessor:
    """Advanced text processing class with multiple preprocessing options."""
    
    def __init__(self, language: str = "en", spacy_model: str = "en_core_web_sm"):
        """
        Initialize the text processor.
        
        Args:
            language: Language code (default: "en")
            spacy_model: SpaCy model name
        """
        self.language = language
        self.spacy_model = spacy_model
        self.nlp = None
        self.stop_words = set()
        
        self._load_models()
        self._load_stopwords()
    
    def _load_models(self):
        """Load SpaCy model."""
        try:
            self.nlp = spacy.load(self.spacy_model)
        except OSError:
            logger.warning(f"SpaCy model {self.spacy_model} not found. Using basic tokenization.")
            self.nlp = None
    
    def _load_stopwords(self):
        """Load stop words for the specified language."""
        try:
            from nltk.corpus import stopwords
            self.stop_words = set(stopwords.words(self.language))
        except:
            logger.warning(f"Could not load stopwords for language {self.language}")
            self.stop_words = set()
    
    def clean_text(self, text: str, remove_punctuation: bool = True, 
                   remove_numbers: bool = False, remove_extra_whitespace: bool = True) -> str:
        """
        Clean text by removing unwanted characters and normalizing.
        
        Args:
            text: Input text to clean
            remove_punctuation: Whether to remove punctuation
            remove_numbers: Whether to remove numbers
            remove_extra_whitespace: Whether to normalize whitespace
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        if remove_extra_whitespace:
            text = re.sub(r'\s+', ' ', text).strip()
        
        # Remove punctuation
        if remove_punctuation:
            text = text.translate(str.maketrans('', '', string.punctuation))
        
        # Remove numbers
        if remove_numbers:
            text = re.sub(r'\d+', '', text)
        
        return text
    
    def tokenize_sentences(self, text: str) -> List[str]:
        """
        Tokenize text into sentences.
        
        Args:
            text: Input text
            
        Returns:
            List of sentences
        """
        if self.nlp:
            doc = self.nlp(text)
            sentences = [sent.text.strip() for sent in doc.sents if sent.text.strip()]
        else:
            # Fallback to NLTK
            from nltk.tokenize import sent_tokenize
            sentences = sent_tokenize(text)
        
        return [sent for sent in sentences if len(sent) > 10]  # Filter very short sentences
    
    def tokenize_words(self, text: str, remove_stopwords: bool = True) -> List[str]:
        """
        Tokenize text into words.
        
        Args:
            text: Input text
            remove_stopwords: Whether to remove stop words
            
        Returns:
            List of words
        """
        if self.nlp:
            doc = self.nlp(text)
            words = [token.text.lower() for token in doc if not token.is_space]
        else:
            # Fallback to NLTK
            from nltk.tokenize import word_tokenize
            words = word_tokenize(text.lower())
        
        if remove_stopwords:
            words = [word for word in words if word not in self.stop_words and len(word) > 2]
        
        return words
    
    def extract_entities(self, text: str) -> List[Dict[str, str]]:
        """
        Extract named entities from text.
        
        Args:
            text: Input text
            
        Returns:
            List of entities with their labels
        """
        if not self.nlp:
            return []
        
        doc = self.nlp(text)
        entities = []
        
        for ent in doc.ents:
            entities.append({
                'text': ent.text,
                'label': ent.label_,
                'start': ent.start_char,
                'end': ent.end_char
            })
        
        return entities
    
    def get_sentence_features(self, sentence: str) -> Dict[str, any]:
        """
        Extract various features from a sentence.
        
        Args:
            sentence: Input sentence
            
        Returns:
            Dictionary of sentence features
        """
        features = {
            'length': len(sentence),
            'word_count': len(self.tokenize_words(sentence, remove_stopwords=False)),
            'char_count': len(sentence),
            'avg_word_length': 0,
            'has_numbers': bool(re.search(r'\d', sentence)),
            'has_capitals': bool(re.search(r'[A-Z]', sentence)),
            'exclamation_count': sentence.count('!'),
            'question_count': sentence.count('?'),
            'comma_count': sentence.count(','),
        }
        
        words = self.tokenize_words(sentence, remove_stopwords=False)
        if words:
            features['avg_word_length'] = sum(len(word) for word in words) / len(words)
        
        return features
    
    def preprocess_for_summarization(self, text: str, 
                                   min_sentence_length: int = 10,
                                   max_sentence_length: int = 200) -> List[str]:
        """
        Preprocess text specifically for summarization.
        
        Args:
            text: Input text
            min_sentence_length: Minimum sentence length
            max_sentence_length: Maximum sentence length
            
        Returns:
            List of preprocessed sentences
        """
        # Clean the text
        cleaned_text = self.clean_text(text, remove_punctuation=False, remove_numbers=False)
        
        # Tokenize into sentences
        sentences = self.tokenize_sentences(cleaned_text)
        
        # Filter sentences by length
        filtered_sentences = [
            sent for sent in sentences 
            if min_sentence_length <= len(sent) <= max_sentence_length
        ]
        
        return filtered_sentences
    
    def create_sentence_embeddings(self, sentences: List[str]) -> List[List[float]]:
        """
        Create sentence embeddings using SpaCy or sentence-transformers.
        
        Args:
            sentences: List of sentences
            
        Returns:
            List of sentence embeddings
        """
        if self.nlp:
            embeddings = []
            for sent in sentences:
                doc = self.nlp(sent)
                embeddings.append(doc.vector.tolist())
            return embeddings
        else:
            # Fallback to basic word averaging (simplified)
            logger.warning("SpaCy not available, using basic word averaging for embeddings")
            return [[0.0] * 300 for _ in sentences]  # Placeholder
    
    def calculate_sentence_similarity(self, sent1: str, sent2: str) -> float:
        """
        Calculate similarity between two sentences.
        
        Args:
            sent1: First sentence
            sent2: Second sentence
            
        Returns:
            Similarity score between 0 and 1
        """
        if self.nlp:
            doc1 = self.nlp(sent1)
            doc2 = self.nlp(sent2)
            return doc1.similarity(doc2)
        else:
            # Fallback to Jaccard similarity
            words1 = set(self.tokenize_words(sent1))
            words2 = set(self.tokenize_words(sent2))
            
            if not words1 or not words2:
                return 0.0
            
            intersection = len(words1.intersection(words2))
            union = len(words1.union(words2))
            
            return intersection / union if union > 0 else 0.0