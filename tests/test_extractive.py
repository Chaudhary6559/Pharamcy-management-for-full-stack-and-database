"""
Tests for extractive summarization methods.
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from src.extractive import TextRankSummarizer, BERTExtractiveSummarizer, LexRankSummarizer


class TestTextRankSummarizer:
    """Test TextRank summarizer."""
    
    def test_initialization(self):
        """Test TextRank initializer."""
        summarizer = TextRankSummarizer()
        assert summarizer is not None
        assert not summarizer.is_loaded
    
    def test_config_loading(self):
        """Test configuration loading."""
        config = {'damping': 0.9, 'max_iter': 50}
        summarizer = TextRankSummarizer(config)
        assert summarizer.damping == 0.9
        assert summarizer.max_iter == 50
    
    def test_load_model(self):
        """Test model loading."""
        summarizer = TextRankSummarizer()
        summarizer.load_model()
        assert summarizer.is_loaded
    
    def test_summarize(self):
        """Test summarization."""
        summarizer = TextRankSummarizer()
        summarizer.load_model()
        
        text = "This is a test sentence. This is another test sentence. This is a third test sentence."
        result = summarizer.summarize(text, num_sentences=2)
        
        assert 'summary' in result
        assert 'sentences' in result
        assert 'method' in result
        assert result['method'] == 'TextRankSummarizer'
        assert len(result['sentences']) <= 2


class TestBERTExtractiveSummarizer:
    """Test BERT extractive summarizer."""
    
    def test_initialization(self):
        """Test BERT extractive initializer."""
        summarizer = BERTExtractiveSummarizer()
        assert summarizer is not None
        assert not summarizer.is_loaded
    
    def test_config_loading(self):
        """Test configuration loading."""
        config = {'model_name': 'sentence-transformers/all-MiniLM-L6-v2'}
        summarizer = BERTExtractiveSummarizer(config)
        assert summarizer.model_name == 'sentence-transformers/all-MiniLM-L6-v2'
    
    @pytest.mark.slow
    def test_load_model(self):
        """Test model loading."""
        summarizer = BERTExtractiveSummarizer()
        summarizer.load_model()
        assert summarizer.is_loaded
    
    @pytest.mark.slow
    def test_summarize(self):
        """Test summarization."""
        summarizer = BERTExtractiveSummarizer()
        summarizer.load_model()
        
        text = "This is a test sentence. This is another test sentence. This is a third test sentence."
        result = summarizer.summarize(text, num_sentences=2)
        
        assert 'summary' in result
        assert 'sentences' in result
        assert 'method' in result
        assert result['method'] == 'BERTExtractiveSummarizer'
        assert len(result['sentences']) <= 2


class TestLexRankSummarizer:
    """Test LexRank summarizer."""
    
    def test_initialization(self):
        """Test LexRank initializer."""
        summarizer = LexRankSummarizer()
        assert summarizer is not None
        assert not summarizer.is_loaded
    
    def test_config_loading(self):
        """Test configuration loading."""
        config = {'threshold': 0.2}
        summarizer = LexRankSummarizer(config)
        assert summarizer.threshold == 0.2
    
    def test_load_model(self):
        """Test model loading."""
        summarizer = LexRankSummarizer()
        summarizer.load_model()
        assert summarizer.is_loaded
    
    def test_summarize(self):
        """Test summarization."""
        summarizer = LexRankSummarizer()
        summarizer.load_model()
        
        text = "This is a test sentence. This is another test sentence. This is a third test sentence."
        result = summarizer.summarize(text, num_sentences=2)
        
        assert 'summary' in result
        assert 'sentences' in result
        assert 'method' in result
        assert result['method'] == 'LexRankSummarizer'
        assert len(result['sentences']) <= 2


if __name__ == "__main__":
    pytest.main([__file__])