"""
Basic usage example for the Hybrid Text Summarization System.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from src.hybrid import HybridSummarizer
from src.evaluation import Evaluator
from src.utils.data_loader import DataLoader
from src.utils.config_loader import ConfigLoader
from src.utils.logger import setup_logger

def main():
    """Basic usage example."""
    # Setup logging
    logger = setup_logger()
    
    # Sample text
    sample_text = """
    Artificial intelligence (AI) is intelligence demonstrated by machines, in contrast to the natural intelligence displayed by humans and animals. Leading AI textbooks define the field as the study of 'intelligent agents': any device that perceives its environment and takes actions that maximize its chance of successfully achieving its goals. Colloquially, the term 'artificial intelligence' is often used to describe machines (or computers) that mimic 'cognitive' functions that humans associate with the human mind, such as 'learning' and 'problem solving'.
    
    Machine learning is a subset of artificial intelligence (AI) that provides systems the ability to automatically learn and improve from experience without being explicitly programmed. Machine learning focuses on the development of computer programs that can access data and use it to learn for themselves. The process of learning begins with observations or data, such as examples, direct experience, or instruction, in order to look for patterns in data and make better decisions in the future based on the examples that we provide.
    
    Deep learning is part of a broader family of machine learning methods based on artificial neural networks with representation learning. Learning can be supervised, semi-supervised or unsupervised. Deep learning architectures such as deep neural networks, deep belief networks, graph neural networks, and recurrent neural networks have been applied to fields including computer vision, speech recognition, natural language processing, machine translation, bioinformatics, drug design, medical image analysis, material inspection and board game programs.
    """
    
    print("🚀 Hybrid Text Summarization System - Basic Usage Example")
    print("=" * 60)
    
    try:
        # Initialize configuration
        config_loader = ConfigLoader()
        
        # Initialize hybrid summarizer
        print("📋 Initializing hybrid summarizer...")
        summarizer = HybridSummarizer(config_loader=config_loader)
        
        # Load models
        print("🔄 Loading models...")
        summarizer.load_models()
        print("✅ Models loaded successfully!")
        
        # Generate summary
        print("\n📝 Generating summary...")
        result = summarizer.summarize(
            text=sample_text,
            num_sentences=3,
            max_length=100,
            min_length=30,
            return_details=True
        )
        
        # Display results
        print("\n📊 Summary Results:")
        print("-" * 40)
        print(f"Method: {result['method']}")
        print(f"Combination Strategy: {result.get('combination_strategy', 'N/A')}")
        print(f"Extractive Weight: {result.get('extractive_weight', 'N/A')}")
        print(f"Abstractive Weight: {result.get('abstractive_weight', 'N/A')}")
        
        print(f"\n📋 Generated Summary:")
        print("-" * 40)
        print(result['summary'])
        
        # Display details if available
        if 'details' in result:
            print(f"\n🔍 Detailed Information:")
            print("-" * 40)
            details = result['details']
            
            if 'extractive_result' in details and details['extractive_result']:
                ext_result = details['extractive_result']
                print(f"Extractive Model: {details.get('extractive_model', 'N/A')}")
                print(f"Extracted Sentences: {ext_result.get('num_sentences', 'N/A')}")
            
            if 'abstractive_result' in details and details['abstractive_result']:
                abs_result = details['abstractive_result']
                print(f"Abstractive Model: {details.get('abstractive_model', 'N/A')}")
                if 'details' in abs_result:
                    abs_details = abs_result['details']
                    print(f"Input Length: {abs_details.get('input_length', 'N/A')}")
                    print(f"Output Length: {abs_details.get('output_length', 'N/A')}")
                    print(f"Compression Ratio: {abs_details.get('compression_ratio', 'N/A'):.2f}")
        
        # Example of evaluation
        print(f"\n📈 Evaluation Example:")
        print("-" * 40)
        
        # Create sample data for evaluation
        data_loader = DataLoader()
        sample_data = data_loader.create_sample_data(3)
        
        # Generate predictions
        predictions = []
        references = []
        
        for item in sample_data:
            pred_result = summarizer.summarize(item['text'], num_sentences=2)
            predictions.append(pred_result['summary'])
            references.append(item['summary'])
        
        # Evaluate
        evaluator = Evaluator(config_loader=config_loader)
        evaluation_results = evaluator.evaluate(predictions, references)
        
        print("Evaluation Results:")
        for metric, scores in evaluation_results.items():
            if metric != 'metadata' and metric != 'overall_score':
                if isinstance(scores, dict) and 'f1' in scores:
                    print(f"  {metric}: {scores['f1']:.3f}")
                elif isinstance(scores, dict) and 'bleu' in scores:
                    print(f"  {metric}: {scores['bleu']:.3f}")
        
        if 'overall_score' in evaluation_results:
            print(f"  Overall Score: {evaluation_results['overall_score']:.3f}")
        
        print(f"\n✅ Example completed successfully!")
        
    except Exception as e:
        logger.error(f"Error in basic usage example: {str(e)}")
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()