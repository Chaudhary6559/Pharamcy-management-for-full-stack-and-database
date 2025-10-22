"""
Command-line interface for hybrid text summarization.
"""

import argparse
import sys
import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.hybrid import HybridSummarizer
from src.evaluation import Evaluator
from src.utils.data_loader import DataLoader
from src.utils.config_loader import ConfigLoader
from src.utils.logger import setup_logger


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Hybrid Text Summarization System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Summarize a single text
  python -m src.cli.main --text "Your text here" --output summary.txt

  # Summarize from file
  python -m src.cli.main --input input.txt --output summary.txt

  # Evaluate on dataset
  python -m src.cli.main --evaluate --data data.json --output results.json

  # Use specific models
  python -m src.cli.main --text "Your text" --extractive textrank --abstractive t5
        """
    )
    
    # Input options
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('--text', type=str, help='Text to summarize')
    input_group.add_argument('--input', type=str, help='Input file path')
    input_group.add_argument('--evaluate', action='store_true', help='Evaluation mode')
    
    # Output options
    parser.add_argument('--output', type=str, help='Output file path')
    parser.add_argument('--format', type=str, choices=['txt', 'json', 'html'], 
                       default='txt', help='Output format')
    
    # Model options
    parser.add_argument('--extractive', type=str, 
                       choices=['textrank', 'bert', 'lexrank'],
                       default='textrank', help='Extractive model to use')
    parser.add_argument('--abstractive', type=str,
                       choices=['t5', 'bart', 'pegasus'],
                       default='t5', help='Abstractive model to use')
    
    # Summarization options
    parser.add_argument('--num-sentences', type=int, default=5,
                       help='Number of sentences for extractive summarization')
    parser.add_argument('--max-length', type=int, default=150,
                       help='Maximum length for abstractive summarization')
    parser.add_argument('--min-length', type=int, default=30,
                       help='Minimum length for abstractive summarization')
    
    # Evaluation options
    parser.add_argument('--data', type=str, help='Dataset file for evaluation')
    parser.add_argument('--metrics', nargs='+', 
                       choices=['rouge-1', 'rouge-2', 'rouge-l', 'bleu', 'bert_score'],
                       default=['rouge-1', 'rouge-2', 'rouge-l', 'bleu'],
                       help='Metrics to compute for evaluation')
    
    # Configuration options
    parser.add_argument('--config', type=str, default='config.yaml',
                       help='Configuration file path')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose logging')
    parser.add_argument('--device', type=str, choices=['cpu', 'cuda'], 
                       default='auto', help='Device to use')
    
    args = parser.parse_args()
    
    # Setup logging
    log_level = 'DEBUG' if args.verbose else 'INFO'
    logger = setup_logger(level=log_level)
    
    try:
        # Load configuration
        config_loader = ConfigLoader(args.config)
        
        # Set device
        if args.device != 'auto':
            config_loader.set('device', args.device)
        
        # Initialize summarizer
        summarizer = HybridSummarizer(config_loader=config_loader)
        summarizer.load_models()
        
        if args.evaluate:
            # Evaluation mode
            run_evaluation(args, summarizer, config_loader, logger)
        else:
            # Summarization mode
            run_summarization(args, summarizer, logger)
            
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)


def run_summarization(args, summarizer: HybridSummarizer, logger: logging.Logger):
    """Run summarization mode."""
    # Get input text
    if args.text:
        text = args.text
    elif args.input:
        with open(args.input, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        raise ValueError("No input text provided")
    
    # Generate summary
    logger.info("Generating summary...")
    result = summarizer.summarize(
        text=text,
        num_sentences=args.num_sentences,
        max_length=args.max_length,
        min_length=args.min_length,
        return_details=True
    )
    
    # Output results
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        if args.format == 'json':
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
        elif args.format == 'html':
            html_content = create_html_output(result)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
        else:  # txt
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(result['summary'])
    else:
        # Print to stdout
        if args.format == 'json':
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(result['summary'])
    
    logger.info("Summarization completed successfully")


def run_evaluation(args, summarizer: HybridSummarizer, config_loader: ConfigLoader, 
                  logger: logging.Logger):
    """Run evaluation mode."""
    if not args.data:
        raise ValueError("Dataset file required for evaluation")
    
    # Load dataset
    data_loader = DataLoader()
    dataset = data_loader.load_from_file(args.data)
    
    if not dataset:
        raise ValueError("No data found in dataset file")
    
    # Prepare data
    texts = [item['text'] for item in dataset]
    references = [item.get('summary', '') for item in dataset]
    
    if not all(references):
        raise ValueError("Reference summaries required for evaluation")
    
    # Generate predictions
    logger.info(f"Generating summaries for {len(texts)} texts...")
    predictions = []
    
    for i, text in enumerate(texts):
        logger.info(f"Processing text {i+1}/{len(texts)}")
        result = summarizer.summarize(
            text=text,
            num_sentences=args.num_sentences,
            max_length=args.max_length,
            min_length=args.min_length
        )
        predictions.append(result['summary'])
    
    # Evaluate
    logger.info("Evaluating summaries...")
    evaluator = Evaluator(config_loader=config_loader)
    evaluation_results = evaluator.evaluate(predictions, references, args.metrics)
    
    # Output results
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(evaluation_results, f, indent=2, ensure_ascii=False)
    else:
        print(json.dumps(evaluation_results, indent=2, ensure_ascii=False))
    
    logger.info("Evaluation completed successfully")


def create_html_output(result: Dict[str, Any]) -> str:
    """Create HTML output for summarization results."""
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Text Summarization Results</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            .summary {{ background-color: #f5f5f5; padding: 20px; border-radius: 5px; }}
            .details {{ margin-top: 20px; }}
            .method {{ color: #666; font-style: italic; }}
        </style>
    </head>
    <body>
        <h1>Text Summarization Results</h1>
        <div class="summary">
            <h2>Summary</h2>
            <p>{result['summary']}</p>
        </div>
        <div class="details">
            <h2>Details</h2>
            <p class="method">Method: {result['method']}</p>
            <p>Combination Strategy: {result.get('combination_strategy', 'N/A')}</p>
            <p>Extractive Weight: {result.get('extractive_weight', 'N/A')}</p>
            <p>Abstractive Weight: {result.get('abstractive_weight', 'N/A')}</p>
        </div>
    </body>
    </html>
    """
    return html


if __name__ == '__main__':
    main()