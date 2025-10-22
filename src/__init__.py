"""
Hybrid Text Summarization Package

A comprehensive text summarization system combining extractive and abstractive methods
using state-of-the-art machine learning and deep learning algorithms.
"""

__version__ = "1.0.0"
__author__ = "Research Team"
__email__ = "research@example.com"

from .extractive import ExtractiveSummarizer
from .abstractive import AbstractiveSummarizer
from .hybrid import HybridSummarizer
from .evaluation import Evaluator

__all__ = [
    "ExtractiveSummarizer",
    "AbstractiveSummarizer", 
    "HybridSummarizer",
    "Evaluator"
]