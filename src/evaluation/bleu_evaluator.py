"""
BLEU evaluation metrics for text summarization.
"""

from typing import List, Dict, Any
import logging
from sacrebleu import BLEU

logger = logging.getLogger(__name__)


class BLEUEvaluator:
    """BLEU evaluation metrics implementation."""
    
    def __init__(self):
        """Initialize BLEU evaluator."""
        self.bleu = BLEU()
    
    def evaluate(self, predictions: List[str], references: List[str]) -> Dict[str, Any]:
        """
        Evaluate predictions against references using BLEU metrics.
        
        Args:
            predictions: List of predicted summaries
            references: List of reference summaries
            
        Returns:
            Dictionary containing BLEU scores
        """
        if len(predictions) != len(references):
            raise ValueError("Number of predictions must match number of references")
        
        # Calculate BLEU score
        bleu_score = self.bleu.corpus_score(predictions, [references])
        
        results = {
            'bleu': {
                'bleu': bleu_score.score / 100.0,  # Convert to 0-1 scale
                'precisions': [p / 100.0 for p in bleu_score.precisions],
                'bp': bleu_score.bp,
                'ratio': bleu_score.ratio,
                'hyp_len': bleu_score.sys_len,
                'ref_len': bleu_score.ref_len
            }
        }
        
        return results
    
    def evaluate_single(self, prediction: str, reference: str) -> Dict[str, Any]:
        """
        Evaluate a single prediction against a single reference.
        
        Args:
            prediction: Predicted summary
            reference: Reference summary
            
        Returns:
            Dictionary containing BLEU scores
        """
        return self.evaluate([prediction], [reference])
    
    def get_detailed_scores(self, predictions: List[str], references: List[str]) -> List[Dict[str, Any]]:
        """
        Get detailed BLEU scores for each prediction-reference pair.
        
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
            # Calculate BLEU for individual pair
            bleu_score = self.bleu.sentence_score(pred, [ref])
            
            detailed_scores.append({
                'bleu': {
                    'bleu': bleu_score.score / 100.0,
                    'precisions': [p / 100.0 for p in bleu_score.precisions],
                    'bp': bleu_score.bp,
                    'ratio': bleu_score.ratio,
                    'hyp_len': bleu_score.sys_len,
                    'ref_len': bleu_score.ref_len
                }
            })
        
        return detailed_scores