"""
Main evaluator class for text summarization metrics.
"""

from typing import List, Dict, Any, Optional, Union
import logging
from .rouge_evaluator import ROUGEEvaluator
from .bleu_evaluator import BLEUEvaluator
from .bert_score_evaluator import BERTScoreEvaluator
from ..utils.config_loader import ConfigLoader

logger = logging.getLogger(__name__)


class Evaluator:
    """Main evaluator class for text summarization metrics."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None,
                 config_loader: Optional[ConfigLoader] = None):
        """
        Initialize the evaluator.
        
        Args:
            config: Configuration dictionary
            config_loader: Configuration loader instance
        """
        self.config = config or {}
        self.config_loader = config_loader or ConfigLoader()
        
        # Initialize individual evaluators
        self.rouge_evaluator = ROUGEEvaluator()
        self.bleu_evaluator = BLEUEvaluator()
        self.bert_score_evaluator = BERTScoreEvaluator()
        
        # Get evaluation configuration
        self.eval_config = self.config_loader.get_evaluation_config()
        self.metrics = self.eval_config.get('metrics', ['rouge-1', 'rouge-2', 'rouge-l', 'bleu'])
    
    def evaluate(self, predictions: List[str], references: List[str], 
                 metrics: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Evaluate predictions against references using specified metrics.
        
        Args:
            predictions: List of predicted summaries
            references: List of reference summaries
            metrics: List of metrics to compute (default: all available)
            
        Returns:
            Dictionary containing evaluation results
        """
        if len(predictions) != len(references):
            raise ValueError("Number of predictions must match number of references")
        
        if not predictions or not references:
            raise ValueError("Predictions and references cannot be empty")
        
        metrics_to_use = metrics or self.metrics
        results = {}
        
        try:
            # ROUGE metrics
            if any(metric.startswith('rouge') for metric in metrics_to_use):
                rouge_results = self.rouge_evaluator.evaluate(predictions, references)
                results.update(rouge_results)
            
            # BLEU metrics
            if 'bleu' in metrics_to_use:
                bleu_results = self.bleu_evaluator.evaluate(predictions, references)
                results.update(bleu_results)
            
            # BERTScore metrics
            if 'bert_score' in metrics_to_use:
                bert_score_results = self.bert_score_evaluator.evaluate(predictions, references)
                results.update(bert_score_results)
            
            # Calculate overall score
            results['overall_score'] = self._calculate_overall_score(results)
            
            # Add metadata
            results['metadata'] = {
                'num_samples': len(predictions),
                'metrics_computed': metrics_to_use,
                'evaluation_timestamp': self._get_timestamp()
            }
            
            return results
            
        except Exception as e:
            logger.error(f"Error during evaluation: {str(e)}")
            raise
    
    def evaluate_single(self, prediction: str, reference: str,
                       metrics: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Evaluate a single prediction against a single reference.
        
        Args:
            prediction: Predicted summary
            reference: Reference summary
            metrics: List of metrics to compute
            
        Returns:
            Dictionary containing evaluation results
        """
        return self.evaluate([prediction], [reference], metrics)
    
    def evaluate_batch(self, predictions: List[str], references: List[str],
                      metrics: Optional[List[str]] = None,
                      batch_size: int = 32) -> Dict[str, Any]:
        """
        Evaluate predictions in batches for memory efficiency.
        
        Args:
            predictions: List of predicted summaries
            references: List of reference summaries
            metrics: List of metrics to compute
            batch_size: Batch size for processing
            
        Returns:
            Dictionary containing evaluation results
        """
        if len(predictions) != len(references):
            raise ValueError("Number of predictions must match number of references")
        
        all_results = []
        
        # Process in batches
        for i in range(0, len(predictions), batch_size):
            batch_predictions = predictions[i:i + batch_size]
            batch_references = references[i:i + batch_size]
            
            batch_results = self.evaluate(batch_predictions, batch_references, metrics)
            all_results.append(batch_results)
        
        # Combine results
        combined_results = self._combine_batch_results(all_results)
        return combined_results
    
    def _calculate_overall_score(self, results: Dict[str, Any]) -> float:
        """
        Calculate overall score from individual metrics.
        
        Args:
            results: Dictionary containing individual metric results
            
        Returns:
            Overall score
        """
        scores = []
        
        # ROUGE scores
        if 'rouge-1' in results:
            scores.append(results['rouge-1']['f1'])
        if 'rouge-2' in results:
            scores.append(results['rouge-2']['f1'])
        if 'rouge-l' in results:
            scores.append(results['rouge-l']['f1'])
        
        # BLEU score
        if 'bleu' in results:
            scores.append(results['bleu']['bleu'])
        
        # BERTScore
        if 'bert_score' in results:
            scores.append(results['bert_score']['f1'])
        
        if not scores:
            return 0.0
        
        return sum(scores) / len(scores)
    
    def _combine_batch_results(self, batch_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Combine results from multiple batches.
        
        Args:
            batch_results: List of batch results
            
        Returns:
            Combined results
        """
        if not batch_results:
            return {}
        
        if len(batch_results) == 1:
            return batch_results[0]
        
        # Initialize combined results
        combined = {}
        
        # Get all metric names
        all_metrics = set()
        for result in batch_results:
            all_metrics.update(result.keys())
        
        # Combine each metric
        for metric in all_metrics:
            if metric in ['metadata', 'overall_score']:
                continue
            
            metric_values = []
            for result in batch_results:
                if metric in result and isinstance(result[metric], dict):
                    if 'f1' in result[metric]:
                        metric_values.append(result[metric]['f1'])
                    elif 'bleu' in result[metric]:
                        metric_values.append(result[metric]['bleu'])
                    elif 'precision' in result[metric]:
                        metric_values.append(result[metric]['precision'])
                    elif 'recall' in result[metric]:
                        metric_values.append(result[metric]['recall'])
            
            if metric_values:
                combined[metric] = {
                    'mean': sum(metric_values) / len(metric_values),
                    'std': self._calculate_std(metric_values),
                    'min': min(metric_values),
                    'max': max(metric_values)
                }
        
        # Calculate overall score
        combined['overall_score'] = self._calculate_overall_score(combined)
        
        # Add metadata
        total_samples = sum(result.get('metadata', {}).get('num_samples', 0) for result in batch_results)
        combined['metadata'] = {
            'num_samples': total_samples,
            'num_batches': len(batch_results),
            'evaluation_timestamp': self._get_timestamp()
        }
        
        return combined
    
    def _calculate_std(self, values: List[float]) -> float:
        """Calculate standard deviation."""
        if len(values) <= 1:
            return 0.0
        
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / (len(values) - 1)
        return variance ** 0.5
    
    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def get_available_metrics(self) -> List[str]:
        """Get list of available metrics."""
        return ['rouge-1', 'rouge-2', 'rouge-l', 'bleu', 'bert_score']
    
    def get_metric_info(self, metric: str) -> Dict[str, Any]:
        """
        Get information about a specific metric.
        
        Args:
            metric: Metric name
            
        Returns:
            Dictionary containing metric information
        """
        metric_info = {
            'rouge-1': {
                'name': 'ROUGE-1',
                'description': 'Unigram overlap between prediction and reference',
                'range': [0, 1],
                'higher_is_better': True
            },
            'rouge-2': {
                'name': 'ROUGE-2',
                'description': 'Bigram overlap between prediction and reference',
                'range': [0, 1],
                'higher_is_better': True
            },
            'rouge-l': {
                'name': 'ROUGE-L',
                'description': 'Longest common subsequence overlap',
                'range': [0, 1],
                'higher_is_better': True
            },
            'bleu': {
                'name': 'BLEU',
                'description': 'Bilingual Evaluation Understudy score',
                'range': [0, 1],
                'higher_is_better': True
            },
            'bert_score': {
                'name': 'BERTScore',
                'description': 'BERT-based semantic similarity score',
                'range': [0, 1],
                'higher_is_better': True
            }
        }
        
        return metric_info.get(metric, {
            'name': metric,
            'description': 'Unknown metric',
            'range': [0, 1],
            'higher_is_better': True
        })