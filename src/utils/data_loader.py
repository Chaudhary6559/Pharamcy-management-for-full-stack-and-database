"""
Data loading utilities for handling various text datasets and formats.
"""

import json
import csv
import pandas as pd
from typing import List, Dict, Any, Optional, Union
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class DataLoader:
    """Data loader for various text datasets and formats."""
    
    def __init__(self):
        """Initialize the data loader."""
        self.supported_formats = ['.json', '.csv', '.txt', '.jsonl']
    
    def load_from_file(self, file_path: str, 
                      text_column: str = 'text',
                      summary_column: str = 'summary',
                      encoding: str = 'utf-8') -> List[Dict[str, Any]]:
        """
        Load data from a file.
        
        Args:
            file_path: Path to the data file
            text_column: Name of the text column
            summary_column: Name of the summary column
            encoding: File encoding
            
        Returns:
            List of dictionaries containing text and summary pairs
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if file_path.suffix not in self.supported_formats:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")
        
        try:
            if file_path.suffix == '.json':
                return self._load_json(file_path, text_column, summary_column, encoding)
            elif file_path.suffix == '.csv':
                return self._load_csv(file_path, text_column, summary_column, encoding)
            elif file_path.suffix == '.txt':
                return self._load_txt(file_path, encoding)
            elif file_path.suffix == '.jsonl':
                return self._load_jsonl(file_path, text_column, summary_column, encoding)
        except Exception as e:
            logger.error(f"Error loading file {file_path}: {str(e)}")
            raise
    
    def _load_json(self, file_path: Path, text_column: str, 
                   summary_column: str, encoding: str) -> List[Dict[str, Any]]:
        """Load data from JSON file."""
        with open(file_path, 'r', encoding=encoding) as f:
            data = json.load(f)
        
        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            return [data]
        else:
            raise ValueError("Invalid JSON format")
    
    def _load_csv(self, file_path: Path, text_column: str, 
                  summary_column: str, encoding: str) -> List[Dict[str, Any]]:
        """Load data from CSV file."""
        df = pd.read_csv(file_path, encoding=encoding)
        
        if text_column not in df.columns:
            raise ValueError(f"Text column '{text_column}' not found in CSV")
        
        data = []
        for _, row in df.iterrows():
            item = {'text': row[text_column]}
            if summary_column in df.columns:
                item['summary'] = row[summary_column]
            data.append(item)
        
        return data
    
    def _load_txt(self, file_path: Path, encoding: str) -> List[Dict[str, Any]]:
        """Load data from plain text file."""
        with open(file_path, 'r', encoding=encoding) as f:
            text = f.read()
        
        return [{'text': text}]
    
    def _load_jsonl(self, file_path: Path, text_column: str, 
                    summary_column: str, encoding: str) -> List[Dict[str, Any]]:
        """Load data from JSONL file."""
        data = []
        with open(file_path, 'r', encoding=encoding) as f:
            for line in f:
                if line.strip():
                    item = json.loads(line)
                    if text_column in item:
                        data.append(item)
        
        return data
    
    def load_dataset(self, dataset_name: str, split: str = 'train') -> List[Dict[str, Any]]:
        """
        Load a standard dataset using Hugging Face datasets.
        
        Args:
            dataset_name: Name of the dataset
            split: Dataset split (train, validation, test)
            
        Returns:
            List of data samples
        """
        try:
            from datasets import load_dataset
            
            dataset = load_dataset(dataset_name, split=split)
            return [item for item in dataset]
        except Exception as e:
            logger.error(f"Error loading dataset {dataset_name}: {str(e)}")
            raise
    
    def save_data(self, data: List[Dict[str, Any]], file_path: str, 
                  format: str = 'json', encoding: str = 'utf-8'):
        """
        Save data to a file.
        
        Args:
            data: Data to save
            file_path: Output file path
            format: Output format (json, csv, txt)
            encoding: File encoding
        """
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        if format == 'json':
            with open(file_path, 'w', encoding=encoding) as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        elif format == 'csv':
            df = pd.DataFrame(data)
            df.to_csv(file_path, index=False, encoding=encoding)
        elif format == 'txt':
            with open(file_path, 'w', encoding=encoding) as f:
                for item in data:
                    f.write(f"Text: {item.get('text', '')}\n")
                    f.write(f"Summary: {item.get('summary', '')}\n\n")
        else:
            raise ValueError(f"Unsupported output format: {format}")
    
    def create_sample_data(self, num_samples: int = 10) -> List[Dict[str, Any]]:
        """
        Create sample data for testing.
        
        Args:
            num_samples: Number of sample documents to create
            
        Returns:
            List of sample data
        """
        sample_texts = [
            "Artificial intelligence (AI) is intelligence demonstrated by machines, in contrast to the natural intelligence displayed by humans and animals. Leading AI textbooks define the field as the study of 'intelligent agents': any device that perceives its environment and takes actions that maximize its chance of successfully achieving its goals. Colloquially, the term 'artificial intelligence' is often used to describe machines (or computers) that mimic 'cognitive' functions that humans associate with the human mind, such as 'learning' and 'problem solving'.",
            
            "Machine learning is a subset of artificial intelligence (AI) that provides systems the ability to automatically learn and improve from experience without being explicitly programmed. Machine learning focuses on the development of computer programs that can access data and use it to learn for themselves. The process of learning begins with observations or data, such as examples, direct experience, or instruction, in order to look for patterns in data and make better decisions in the future based on the examples that we provide.",
            
            "Deep learning is part of a broader family of machine learning methods based on artificial neural networks with representation learning. Learning can be supervised, semi-supervised or unsupervised. Deep learning architectures such as deep neural networks, deep belief networks, graph neural networks, and recurrent neural networks have been applied to fields including computer vision, speech recognition, natural language processing, machine translation, bioinformatics, drug design, medical image analysis, material inspection and board game programs.",
            
            "Natural language processing (NLP) is a subfield of linguistics, computer science, and artificial intelligence concerned with the interactions between computers and human language, in particular how to program computers to process and analyze large amounts of natural language data. The goal is a computer capable of 'understanding' the contents of documents, including the contextual nuances of the language within them.",
            
            "Text summarization is the process of creating a short, accurate, and fluent summary of a longer text document while preserving key information and overall meaning. There are two main approaches to automatic text summarization: extractive and abstractive. Extractive summarization involves selecting the most important sentences from the original text, while abstractive summarization generates new sentences that may not appear in the original text."
        ]
        
        sample_summaries = [
            "AI is machine intelligence that perceives environments and takes actions to achieve goals, mimicking human cognitive functions like learning and problem solving.",
            
            "Machine learning is an AI subset that enables systems to automatically learn and improve from experience without explicit programming, focusing on pattern recognition in data.",
            
            "Deep learning uses artificial neural networks for representation learning, with applications in computer vision, NLP, and other fields through supervised, semi-supervised, or unsupervised learning.",
            
            "NLP is a field combining linguistics, computer science, and AI to enable computers to process, analyze, and understand human language data and contextual nuances.",
            
            "Text summarization creates concise summaries of longer documents using extractive (selecting sentences) or abstractive (generating new text) approaches."
        ]
        
        data = []
        for i in range(num_samples):
            text_idx = i % len(sample_texts)
            data.append({
                'text': sample_texts[text_idx],
                'summary': sample_summaries[text_idx],
                'id': f"sample_{i+1}"
            })
        
        return data