"""
BERTScore evaluation metrics for text summarization.
"""

from typing import List, Dict, Any, Optional
import logging
import torch
from bert_score import score as bert_score

logger = logging.getLogger(__name__)


class BERTScoreEvaluator:
    """BERTScore evaluation metrics implementation."""
    
    def __init__(self, model_type: str = "microsoft/DialoGPT-medium", 
                 lang: str = "en", device: Optional[str] = None):
        """
        Initialize BERTScore evaluator.
        
        Args:
            model_type: BERT model type for scoring
            lang: Language code
            device: Device to run on (None for auto-detection)
        """
        self.model_type = model_type
        self.lang = lang
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
    
    def evaluate(self, predictions: List[str], references: List[str]) -> Dict[str, Any]:
        """
        Evaluate predictions against references using BERTScore metrics.
        
        Args:
            predictions: List of predicted summaries
            references: List of reference summaries
            
        Returns:
            Dictionary containing BERTScore results
        """
        if len(predictions) != len(references):
            raise ValueError("Number of predictions must match number of references")
        
        try:
            # Calculate BERTScore
            P, R, F1 = bert_score(
                predictions, 
                references, 
                model_type=self.model_type,
                lang=self.lang,
                device=self.device,
                verbose=False
            )
            
            # Convert to Python floats
            precision = P.mean().item()
            recall = R.mean().item()
            f1 = F1.mean().item()
            
            results = {
                'bert_score': {
                    'precision': precision,
                    'recall': recall,
                    'f1': f1
                }
            }
            
            return results
            
        except Exception as e:
            logger.error(f"Error calculating BERTScore: {str(e)}")
            # Return zero scores if calculation fails
            return {
                'bert_score': {
                    'precision': 0.0,
                    'recall': 0.0,
                    'f1': 0.0
                }
            }
    
    def evaluate_single(self, prediction: str, reference: str) -> Dict[str, Any]:
        """
        Evaluate a single prediction against a single reference.
        
        Args:
            prediction: Predicted summary
            reference: Reference summary
            
        Returns:
            Dictionary containing BERTScore results
        """
        return self.evaluate([prediction], [reference])
    
    def get_detailed_scores(self, predictions: List[str], references: List[str]) -> List[Dict[str, Any]]:
        """
        Get detailed BERTScore for each prediction-reference pair.
        
        Args:
            predictions: List of predicted summaries
            references: List of reference summaries
            
        Returns:
            List of detailed scores for each pair
        """
        if len(predictions) != len(references):
            raise ValueError("Number of predictions must match number of references")
        
        try:
            # Calculate BERTScore with individual scores
            P, R, F1 = bert_score(
                predictions, 
                references, 
                model_type=self.model_type,
                lang=self.lang,
                device=self.device,
                verbose=False
            )
            
            detailed_scores = []
            for i in range(len(predictions)):
                detailed_scores.append({
                    'bert_score': {
                        'precision': P[i].item(),
                        'recall': R[i].item(),
                        'f1': F1[i].item()
                    }
                })
            
            return detailed_scores
            
        except Exception as e:
            logger.error(f"Error calculating detailed BERTScore: {str(e)}")
            # Return zero scores if calculation fails
            return [
                {
                    'bert_score': {
                        'precision': 0.0,
                        'recall': 0.0,
                        'f1': 0.0
                    }
                }
                for _ in range(len(predictions))
            ]
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get BERTScore model information."""
        return {
            'model_type': self.model_type,
            'language': self.lang,
            'device': self.device
        }