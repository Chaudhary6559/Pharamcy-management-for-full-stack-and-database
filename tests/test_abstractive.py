"""
Tests for abstractive summarization methods.
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from src.abstractive import T5Summarizer, BARTSummarizer, PegasusSummarizer


class TestT5Summarizer:
    """Test T5 summarizer."""
    
    def test_initialization(self):
        """Test T5 initializer."""
        summarizer = T5Summarizer()
        assert summarizer is not None
        assert not summarizer.is_loaded
    
    def test_config_loading(self):
        """Test configuration loading."""
        config = {'model_name': 't5-small', 'max_length': 256}
        summarizer = T5Summarizer(config)
        assert summarizer.model_name == 't5-small'
        assert summarizer.max_length == 256
    
    @pytest.mark.slow
    def test_load_model(self):
        """Test model loading."""
        summarizer = T5Summarizer({'model_name': 't5-small'})
        summarizer.load_model()
        assert summarizer.is_loaded
    
    @pytest.mark.slow
    def test_summarize(self):
        """Test summarization."""
        summarizer = T5Summarizer({'model_name': 't5-small'})
        summarizer.load_model()
        
        text = "This is a test sentence. This is another test sentence. This is a third test sentence."
        result = summarizer.summarize(text, max_length=50, min_length=10)
        
        assert 'summary' in result
        assert 'method' in result
        assert result['method'] == 'T5Summarizer'
        assert len(result['summary']) > 0


class TestBARTSummarizer:
    """Test BART summarizer."""
    
    def test_initialization(self):
        """Test BART initializer."""
        summarizer = BARTSummarizer()
        assert summarizer is not None
        assert not summarizer.is_loaded
    
    def test_config_loading(self):
        """Test configuration loading."""
        config = {'model_name': 'facebook/bart-large-cnn', 'max_length': 512}
        summarizer = BARTSummarizer(config)
        assert summarizer.model_name == 'facebook/bart-large-cnn'
        assert summarizer.max_length == 512
    
    @pytest.mark.slow
    def test_load_model(self):
        """Test model loading."""
        summarizer = BARTSummarizer({'model_name': 'facebook/bart-large-cnn'})
        summarizer.load_model()
        assert summarizer.is_loaded
    
    @pytest.mark.slow
    def test_summarize(self):
        """Test summarization."""
        summarizer = BARTSummarizer({'model_name': 'facebook/bart-large-cnn'})
        summarizer.load_model()
        
        text = "This is a test sentence. This is another test sentence. This is a third test sentence."
        result = summarizer.summarize(text, max_length=50, min_length=10)
        
        assert 'summary' in result
        assert 'method' in result
        assert result['method'] == 'BARTSummarizer'
        assert len(result['summary']) > 0


class TestPegasusSummarizer:
    """Test Pegasus summarizer."""
    
    def test_initialization(self):
        """Test Pegasus initializer."""
        summarizer = PegasusSummarizer()
        assert summarizer is not None
        assert not summarizer.is_loaded
    
    def test_config_loading(self):
        """Test configuration loading."""
        config = {'model_name': 'google/pegasus-xsum', 'max_length': 256}
        summarizer = PegasusSummarizer(config)
        assert summarizer.model_name == 'google/pegasus-xsum'
        assert summarizer.max_length == 256
    
    @pytest.mark.slow
    def test_load_model(self):
        """Test model loading."""
        summarizer = PegasusSummarizer({'model_name': 'google/pegasus-xsum'})
        summarizer.load_model()
        assert summarizer.is_loaded
    
    @pytest.mark.slow
    def test_summarize(self):
        """Test summarization."""
        summarizer = PegasusSummarizer({'model_name': 'google/pegasus-xsum'})
        summarizer.load_model()
        
        text = "This is a test sentence. This is another test sentence. This is a third test sentence."
        result = summarizer.summarize(text, max_length=50, min_length=10)
        
        assert 'summary' in result
        assert 'method' in result
        assert result['method'] == 'PegasusSummarizer'
        assert len(result['summary']) > 0


if __name__ == "__main__":
    pytest.main([__file__])