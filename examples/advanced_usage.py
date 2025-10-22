"""
Advanced usage example demonstrating various features of the Hybrid Text Summarization System.
"""

import sys
import json
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from src.extractive import TextRankSummarizer, BERTExtractiveSummarizer, LexRankSummarizer
from src.abstractive import T5Summarizer, BARTSummarizer, PegasusSummarizer
from src.hybrid import HybridSummarizer
from src.evaluation import Evaluator
from src.utils.data_loader import DataLoader
from src.utils.config_loader import ConfigLoader
from src.utils.logger import setup_logger

def compare_extractive_methods():
    """Compare different extractive summarization methods."""
    print("🔍 Comparing Extractive Methods")
    print("=" * 50)
    
    sample_text = """
    Natural language processing (NLP) is a subfield of linguistics, computer science, and artificial intelligence concerned with the interactions between computers and human language, in particular how to program computers to process and analyze large amounts of natural language data. The goal is a computer capable of 'understanding' the contents of documents, including the contextual nuances of the language within them. The technology can then accurately extract information and insights contained in the documents as well as categorize and organize the documents themselves.
    
    Text summarization is the process of creating a short, accurate, and fluent summary of a longer text document while preserving key information and overall meaning. There are two main approaches to automatic text summarization: extractive and abstractive. Extractive summarization involves selecting the most important sentences from the original text, while abstractive summarization generates new sentences that may not appear in the original text.
    
    Machine learning is a subset of artificial intelligence (AI) that provides systems the ability to automatically learn and improve from experience without being explicitly programmed. Machine learning focuses on the development of computer programs that can access data and use it to learn for themselves. The process of learning begins with observations or data, such as examples, direct experience, or instruction, in order to look for patterns in data and make better decisions in the future based on the examples that we provide.
    """
    
    # Initialize extractive summarizers
    textrank = TextRankSummarizer({'damping': 0.85, 'max_iter': 100})
    bert_extractive = BERTExtractiveSummarizer({'model_name': 'sentence-transformers/all-MiniLM-L6-v2'})
    lexrank = LexRankSummarizer({'threshold': 0.1})
    
    methods = {
        "TextRank": textrank,
        "BERT Extractive": bert_extractive,
        "LexRank": lexrank
    }
    
    results = {}
    
    for name, summarizer in methods.items():
        print(f"\n🔄 Running {name}...")
        try:
            summarizer.load_model()
            result = summarizer.summarize(sample_text, num_sentences=3, return_scores=True)
            results[name] = result
            print(f"✅ {name} completed")
        except Exception as e:
            print(f"❌ {name} failed: {str(e)}")
            results[name] = {'summary': '', 'error': str(e)}
    
    # Display results
    print(f"\n📊 Extractive Methods Comparison:")
    print("-" * 50)
    
    for name, result in results.items():
        print(f"\n{name}:")
        if 'error' in result:
            print(f"  Error: {result['error']}")
        else:
            print(f"  Summary: {result['summary']}")
            if 'scores' in result:
                print(f"  Sentence Scores: {len(result['scores'])} sentences scored")

def compare_abstractive_methods():
    """Compare different abstractive summarization methods."""
    print("\n🎯 Comparing Abstractive Methods")
    print("=" * 50)
    
    sample_text = """
    Deep learning is part of a broader family of machine learning methods based on artificial neural networks with representation learning. Learning can be supervised, semi-supervised or unsupervised. Deep learning architectures such as deep neural networks, deep belief networks, graph neural networks, and recurrent neural networks have been applied to fields including computer vision, speech recognition, natural language processing, machine translation, bioinformatics, drug design, medical image analysis, material inspection and board game programs.
    
    Transformers are a type of neural network architecture that has become the foundation for many state-of-the-art natural language processing models. They were introduced in the paper 'Attention Is All You Need' and have since revolutionized the field. The key innovation of transformers is the self-attention mechanism, which allows the model to focus on different parts of the input sequence when processing each element.
    """
    
    # Initialize abstractive summarizers
    t5 = T5Summarizer({'model_name': 't5-small'})
    bart = BARTSummarizer({'model_name': 'facebook/bart-large-cnn'})
    pegasus = PegasusSummarizer({'model_name': 'google/pegasus-xsum'})
    
    methods = {
        "T5": t5,
        "BART": bart,
        "Pegasus": pegasus
    }
    
    results = {}
    
    for name, summarizer in methods.items():
        print(f"\n🔄 Running {name}...")
        try:
            summarizer.load_model()
            result = summarizer.summarize(sample_text, max_length=100, min_length=30, return_details=True)
            results[name] = result
            print(f"✅ {name} completed")
        except Exception as e:
            print(f"❌ {name} failed: {str(e)}")
            results[name] = {'summary': '', 'error': str(e)}
    
    # Display results
    print(f"\n📊 Abstractive Methods Comparison:")
    print("-" * 50)
    
    for name, result in results.items():
        print(f"\n{name}:")
        if 'error' in result:
            print(f"  Error: {result['error']}")
        else:
            print(f"  Summary: {result['summary']}")
            if 'details' in result:
                details = result['details']
                print(f"  Input Length: {details.get('input_length', 'N/A')}")
                print(f"  Output Length: {details.get('output_length', 'N/A')}")
                print(f"  Compression Ratio: {details.get('compression_ratio', 'N/A'):.2f}")

def demonstrate_hybrid_approaches():
    """Demonstrate different hybrid summarization approaches."""
    print("\n🔗 Demonstrating Hybrid Approaches")
    print("=" * 50)
    
    sample_text = """
    Artificial intelligence (AI) is intelligence demonstrated by machines, in contrast to the natural intelligence displayed by humans and animals. Leading AI textbooks define the field as the study of 'intelligent agents': any device that perceives its environment and takes actions that maximize its chance of successfully achieving its goals. Colloquially, the term 'artificial intelligence' is often used to describe machines (or computers) that mimic 'cognitive' functions that humans associate with the human mind, such as 'learning' and 'problem solving'.
    
    Machine learning is a subset of artificial intelligence (AI) that provides systems the ability to automatically learn and improve from experience without being explicitly programmed. Machine learning focuses on the development of computer programs that can access data and use it to learn for themselves. The process of learning begins with observations or data, such as examples, direct experience, or instruction, in order to look for patterns in data and make better decisions in the future based on the examples that we provide.
    
    Deep learning is part of a broader family of machine learning methods based on artificial neural networks with representation learning. Learning can be supervised, semi-supervised or unsupervised. Deep learning architectures such as deep neural networks, deep belief networks, graph neural networks, and recurrent neural networks have been applied to fields including computer vision, speech recognition, natural language processing, machine translation, bioinformatics, drug design, medical image analysis, material inspection and board game programs.
    """
    
    # Different hybrid configurations
    configs = [
        {
            'name': 'Weighted Combination (40% Extractive, 60% Abstractive)',
            'weights': {'extractive': 0.4, 'abstractive': 0.6},
            'strategy': 'weighted_combination'
        },
        {
            'name': 'Pipeline (Extractive → Abstractive)',
            'weights': {'extractive': 0.5, 'abstractive': 0.5},
            'strategy': 'pipeline'
        },
        {
            'name': 'Ensemble (Equal Weight)',
            'weights': {'extractive': 0.5, 'abstractive': 0.5},
            'strategy': 'ensemble'
        }
    ]
    
    results = {}
    
    for config in configs:
        print(f"\n🔄 Running {config['name']}...")
        try:
            # Create custom configuration
            custom_config = {
                'hybrid': {
                    'weights': config['weights'],
                    'combination_strategy': config['strategy']
                }
            }
            
            # Initialize hybrid summarizer with custom config
            config_loader = ConfigLoader()
            for key, value in custom_config.items():
                for sub_key, sub_value in value.items():
                    config_loader.set(f"{key}.{sub_key}", sub_value)
            
            summarizer = HybridSummarizer(config_loader=config_loader)
            summarizer.load_models()
            
            result = summarizer.summarize(
                sample_text, 
                num_sentences=3, 
                max_length=120, 
                min_length=40,
                return_details=True
            )
            
            results[config['name']] = result
            print(f"✅ {config['name']} completed")
            
        except Exception as e:
            print(f"❌ {config['name']} failed: {str(e)}")
            results[config['name']] = {'summary': '', 'error': str(e)}
    
    # Display results
    print(f"\n📊 Hybrid Approaches Comparison:")
    print("-" * 50)
    
    for name, result in results.items():
        print(f"\n{name}:")
        if 'error' in result:
            print(f"  Error: {result['error']}")
        else:
            print(f"  Summary: {result['summary']}")
            print(f"  Strategy: {result.get('combination_strategy', 'N/A')}")
            print(f"  Extractive Weight: {result.get('extractive_weight', 'N/A')}")
            print(f"  Abstractive Weight: {result.get('abstractive_weight', 'N/A')}")

def comprehensive_evaluation():
    """Perform comprehensive evaluation on sample data."""
    print("\n📈 Comprehensive Evaluation")
    print("=" * 50)
    
    # Create sample dataset
    data_loader = DataLoader()
    sample_data = data_loader.create_sample_data(5)
    
    print(f"📊 Created sample dataset with {len(sample_data)} samples")
    
    # Initialize hybrid summarizer
    config_loader = ConfigLoader()
    summarizer = HybridSummarizer(config_loader=config_loader)
    summarizer.load_models()
    
    # Generate predictions
    predictions = []
    references = []
    
    print("🔄 Generating predictions...")
    for i, item in enumerate(sample_data):
        print(f"  Processing sample {i+1}/{len(sample_data)}")
        result = summarizer.summarize(item['text'], num_sentences=2, max_length=100)
        predictions.append(result['summary'])
        references.append(item['summary'])
    
    # Evaluate
    print("📊 Running evaluation...")
    evaluator = Evaluator(config_loader=config_loader)
    evaluation_results = evaluator.evaluate(predictions, references)
    
    # Display results
    print(f"\n📈 Evaluation Results:")
    print("-" * 50)
    
    # ROUGE scores
    if 'rouge-1' in evaluation_results:
        rouge1 = evaluation_results['rouge-1']
        print(f"ROUGE-1: P={rouge1['precision']:.3f}, R={rouge1['recall']:.3f}, F1={rouge1['f1']:.3f}")
    
    if 'rouge-2' in evaluation_results:
        rouge2 = evaluation_results['rouge-2']
        print(f"ROUGE-2: P={rouge2['precision']:.3f}, R={rouge2['recall']:.3f}, F1={rouge2['f1']:.3f}")
    
    if 'rouge-l' in evaluation_results:
        rouge_l = evaluation_results['rouge-l']
        print(f"ROUGE-L: P={rouge_l['precision']:.3f}, R={rouge_l['recall']:.3f}, F1={rouge_l['f1']:.3f}")
    
    # BLEU score
    if 'bleu' in evaluation_results:
        bleu = evaluation_results['bleu']
        print(f"BLEU: {bleu['bleu']:.3f}")
    
    # BERTScore
    if 'bert_score' in evaluation_results:
        bert = evaluation_results['bert_score']
        print(f"BERTScore: P={bert['precision']:.3f}, R={bert['recall']:.3f}, F1={bert['f1']:.3f}")
    
    # Overall score
    if 'overall_score' in evaluation_results:
        print(f"Overall Score: {evaluation_results['overall_score']:.3f}")
    
    # Save results
    output_file = Path(__file__).parent / "evaluation_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(evaluation_results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Results saved to: {output_file}")

def main():
    """Main function for advanced usage example."""
    print("🚀 Hybrid Text Summarization System - Advanced Usage Example")
    print("=" * 70)
    
    try:
        # Compare extractive methods
        compare_extractive_methods()
        
        # Compare abstractive methods
        compare_abstractive_methods()
        
        # Demonstrate hybrid approaches
        demonstrate_hybrid_approaches()
        
        # Comprehensive evaluation
        comprehensive_evaluation()
        
        print(f"\n✅ Advanced usage example completed successfully!")
        
    except Exception as e:
        print(f"❌ Error in advanced usage example: {str(e)}")

if __name__ == "__main__":
    main()