"""
Tests for evaluation metrics.
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from src.evaluation import Evaluator, ROUGEEvaluator, BLEUEvaluator, BERTScoreEvaluator


class TestROUGEEvaluator:
    """Test ROUGE evaluator."""
    
    def test_initialization(self):
        """Test ROUGE evaluator initializer."""
        evaluator = ROUGEEvaluator()
        assert evaluator is not None
        assert evaluator.use_stemmer == True
    
    def test_evaluate(self):
        """Test ROUGE evaluation."""
        evaluator = ROUGEEvaluator()
        
        predictions = ["This is a test summary."]
        references = ["This is a reference summary."]
        
        results = evaluator.evaluate(predictions, references)
        
        assert 'rouge-1' in results
        assert 'rouge-2' in results
        assert 'rouge-l' in results
        
        for metric in ['rouge-1', 'rouge-2', 'rouge-l']:
            assert 'precision' in results[metric]
            assert 'recall' in results[metric]
            assert 'f1' in results[metric]
    
    def test_evaluate_single(self):
        """Test single evaluation."""
        evaluator = ROUGEEvaluator()
        
        prediction = "This is a test summary."
        reference = "This is a reference summary."
        
        results = evaluator.evaluate_single(prediction, reference)
        
        assert 'rouge-1' in results
        assert 'rouge-2' in results
        assert 'rouge-l' in results


class TestBLEUEvaluator:
    """Test BLEU evaluator."""
    
    def test_initialization(self):
        """Test BLEU evaluator initializer."""
        evaluator = BLEUEvaluator()
        assert evaluator is not None
    
    def test_evaluate(self):
        """Test BLEU evaluation."""
        evaluator = BLEUEvaluator()
        
        predictions = ["This is a test summary."]
        references = ["This is a reference summary."]
        
        results = evaluator.evaluate(predictions, references)
        
        assert 'bleu' in results
        assert 'bleu' in results['bleu']
        assert 'precisions' in results['bleu']
        assert 'bp' in results['bleu']
    
    def test_evaluate_single(self):
        """Test single evaluation."""
        evaluator = BLEUEvaluator()
        
        prediction = "This is a test summary."
        reference = "This is a reference summary."
        
        results = evaluator.evaluate_single(prediction, reference)
        
        assert 'bleu' in results
        assert 'bleu' in results['bleu']


class TestBERTScoreEvaluator:
    """Test BERTScore evaluator."""
    
    def test_initialization(self):
        """Test BERTScore evaluator initializer."""
        evaluator = BERTScoreEvaluator()
        assert evaluator is not None
        assert evaluator.model_type == "microsoft/DialoGPT-medium"
    
    @pytest.mark.slow
    def test_evaluate(self):
        """Test BERTScore evaluation."""
        evaluator = BERTScoreEvaluator()
        
        predictions = ["This is a test summary."]
        references = ["This is a reference summary."]
        
        results = evaluator.evaluate(predictions, references)
        
        assert 'bert_score' in results
        assert 'precision' in results['bert_score']
        assert 'recall' in results['bert_score']
        assert 'f1' in results['bert_score']
    
    @pytest.mark.slow
    def test_evaluate_single(self):
        """Test single evaluation."""
        evaluator = BERTScoreEvaluator()
        
        prediction = "This is a test summary."
        reference = "This is a reference summary."
        
        results = evaluator.evaluate_single(prediction, reference)
        
        assert 'bert_score' in results
        assert 'precision' in results['bert_score']


class TestEvaluator:
    """Test main evaluator."""
    
    def test_initialization(self):
        """Test evaluator initializer."""
        evaluator = Evaluator()
        assert evaluator is not None
        assert 'rouge-1' in evaluator.metrics
    
    def test_evaluate(self):
        """Test evaluation."""
        evaluator = Evaluator()
        
        predictions = ["This is a test summary."]
        references = ["This is a reference summary."]
        
        results = evaluator.evaluate(predictions, references)
        
        assert 'overall_score' in results
        assert 'metadata' in results
        assert 'rouge-1' in results
    
    def test_evaluate_single(self):
        """Test single evaluation."""
        evaluator = Evaluator()
        
        prediction = "This is a test summary."
        reference = "This is a reference summary."
        
        results = evaluator.evaluate_single(prediction, reference)
        
        assert 'overall_score' in results
        assert 'metadata' in results
    
    def test_get_available_metrics(self):
        """Test available metrics retrieval."""
        evaluator = Evaluator()
        metrics = evaluator.get_available_metrics()
        
        assert 'rouge-1' in metrics
        assert 'rouge-2' in metrics
        assert 'rouge-l' in metrics
        assert 'bleu' in metrics
        assert 'bert_score' in metrics
    
    def test_get_metric_info(self):
        """Test metric info retrieval."""
        evaluator = Evaluator()
        
        info = evaluator.get_metric_info('rouge-1')
        assert 'name' in info
        assert 'description' in info
        assert 'range' in info
        assert 'higher_is_better' in info


if __name__ == "__main__":
    pytest.main([__file__])