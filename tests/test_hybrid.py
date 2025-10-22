"""
Tests for hybrid summarization methods.
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from src.hybrid import HybridSummarizer
from src.utils.config_loader import ConfigLoader


class TestHybridSummarizer:
    """Test hybrid summarizer."""
    
    def test_initialization(self):
        """Test hybrid summarizer initializer."""
        summarizer = HybridSummarizer()
        assert summarizer is not None
        assert not summarizer.is_loaded
    
    def test_config_loading(self):
        """Test configuration loading."""
        config_loader = ConfigLoader()
        summarizer = HybridSummarizer(config_loader=config_loader)
        assert summarizer.config_loader is not None
    
    @pytest.mark.slow
    def test_load_models(self):
        """Test model loading."""
        summarizer = HybridSummarizer()
        summarizer.load_models()
        assert summarizer.is_loaded
    
    @pytest.mark.slow
    def test_summarize(self):
        """Test summarization."""
        summarizer = HybridSummarizer()
        summarizer.load_models()
        
        text = "This is a test sentence. This is another test sentence. This is a third test sentence."
        result = summarizer.summarize(text, num_sentences=2, max_length=50, min_length=10)
        
        assert 'summary' in result
        assert 'method' in result
        assert result['method'] == 'hybrid'
        assert len(result['summary']) > 0
    
    @pytest.mark.slow
    def test_batch_summarize(self):
        """Test batch summarization."""
        summarizer = HybridSummarizer()
        summarizer.load_models()
        
        texts = [
            "This is the first test text.",
            "This is the second test text.",
            "This is the third test text."
        ]
        
        results = summarizer.batch_summarize(texts, num_sentences=1, max_length=30, min_length=10)
        
        assert len(results) == 3
        for result in results:
            assert 'summary' in result
            assert 'method' in result
            assert result['method'] == 'hybrid'
    
    def test_get_model_info(self):
        """Test model info retrieval."""
        summarizer = HybridSummarizer()
        info = summarizer.get_model_info()
        
        assert 'is_loaded' in info
        assert 'combination_strategy' in info
        assert 'extractive_weight' in info
        assert 'abstractive_weight' in info


if __name__ == "__main__":
    pytest.main([__file__])