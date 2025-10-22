"""
ROUGE evaluation metrics for text summarization.
"""

from typing import List, Dict, Any
import logging
from rouge_score import rouge_scorer

logger = logging.getLogger(__name__)


class ROUGEEvaluator:
    """ROUGE evaluation metrics implementation."""
    
    def __init__(self, use_stemmer: bool = True, rouge_l_max: int = 4):
        """
        Initialize ROUGE evaluator.
        
        Args:
            use_stemmer: Whether to use stemming
            rouge_l_max: Maximum length for ROUGE-L
        """
        self.use_stemmer = use_stemmer
        self.rouge_l_max = rouge_l_max
        
        # Initialize ROUGE scorer
        self.scorer = rouge_scorer.RougeScorer(
            ['rouge1', 'rouge2', 'rougeL'],
            use_stemmer=use_stemmer
        )
    
    def evaluate(self, predictions: List[str], references: List[str]) -> Dict[str, Any]:
        """
        Evaluate predictions against references using ROUGE metrics.
        
        Args:
            predictions: List of predicted summaries
            references: List of reference summaries
            
        Returns:
            Dictionary containing ROUGE scores
        """
        if len(predictions) != len(references):
            raise ValueError("Number of predictions must match number of references")
        
        rouge1_scores = []
        rouge2_scores = []
        rouge_l_scores = []
        
        for pred, ref in zip(predictions, references):
            scores = self.scorer.score(ref, pred)
            
            rouge1_scores.append(scores['rouge1'])
            rouge2_scores.append(scores['rouge2'])
            rouge_l_scores.append(scores['rougeL'])
        
        # Calculate average scores
        results = {}
        
        # ROUGE-1
        rouge1_precision = sum(score.precision for score in rouge1_scores) / len(rouge1_scores)
        rouge1_recall = sum(score.recall for score in rouge1_scores) / len(rouge1_scores)
        rouge1_f1 = sum(score.fmeasure for score in rouge1_scores) / len(rouge1_scores)
        
        results['rouge-1'] = {
            'precision': rouge1_precision,
            'recall': rouge1_recall,
            'f1': rouge1_f1
        }
        
        # ROUGE-2
        rouge2_precision = sum(score.precision for score in rouge2_scores) / len(rouge2_scores)
        rouge2_recall = sum(score.recall for score in rouge2_scores) / len(rouge2_scores)
        rouge2_f1 = sum(score.fmeasure for score in rouge2_scores) / len(rouge2_scores)
        
        results['rouge-2'] = {
            'precision': rouge2_precision,
            'recall': rouge2_recall,
            'f1': rouge2_f1
        }
        
        # ROUGE-L
        rouge_l_precision = sum(score.precision for score in rouge_l_scores) / len(rouge_l_scores)
        rouge_l_recall = sum(score.recall for score in rouge_l_scores) / len(rouge_l_scores)
        rouge_l_f1 = sum(score.fmeasure for score in rouge_l_scores) / len(rouge_l_scores)
        
        results['rouge-l'] = {
            'precision': rouge_l_precision,
            'recall': rouge_l_recall,
            'f1': rouge_l_f1
        }
        
        return results
    
    def evaluate_single(self, prediction: str, reference: str) -> Dict[str, Any]:
        """
        Evaluate a single prediction against a single reference.
        
        Args:
            prediction: Predicted summary
            reference: Reference summary
            
        Returns:
            Dictionary containing ROUGE scores
        """
        return self.evaluate([prediction], [reference])
    
    def get_detailed_scores(self, predictions: List[str], references: List[str]) -> List[Dict[str, Any]]:
        """
        Get detailed ROUGE scores for each prediction-reference pair.
        
        Args:
            predictions: List of predicted summaries
            references: List of reference summaries
            
        Returns:
            List of detailed scores for each pair
        """
        if len(predictions) != len(references):
            raise ValueError("Number of predictions must match number of references")
        
        detailed_scores = []
        
        for pred, ref in zip(predictions, references):
            scores = self.scorer.score(ref, pred)
            
            detailed_scores.append({
                'rouge-1': {
                    'precision': scores['rouge1'].precision,
                    'recall': scores['rouge1'].recall,
                    'f1': scores['rouge1'].fmeasure
                },
                'rouge-2': {
                    'precision': scores['rouge2'].precision,
                    'recall': scores['rouge2'].recall,
                    'f1': scores['rouge2'].fmeasure
                },
                'rouge-l': {
                    'precision': scores['rougeL'].precision,
                    'recall': scores['rougeL'].recall,
                    'f1': scores['rougeL'].fmeasure
                }
            })
        
        return detailed_scores