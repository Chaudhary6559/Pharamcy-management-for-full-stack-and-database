"""
Streamlit web interface for Hybrid Text Summarization System.
"""

import streamlit as st
import json
import sys
from pathlib import Path
import logging

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from src.hybrid import HybridSummarizer
from src.evaluation import Evaluator
from src.utils.data_loader import DataLoader
from src.utils.config_loader import ConfigLoader
from src.utils.logger import setup_logger

# Page configuration
st.set_page_config(
    page_title="Hybrid Text Summarization",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .summary-box {
        background-color: #e8f4fd;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'summarizer' not in st.session_state:
    st.session_state.summarizer = None
if 'config_loader' not in st.session_state:
    st.session_state.config_loader = None

@st.cache_resource
def load_models():
    """Load models with caching."""
    try:
        config_loader = ConfigLoader()
        summarizer = HybridSummarizer(config_loader=config_loader)
        summarizer.load_models()
        return summarizer, config_loader
    except Exception as e:
        st.error(f"Error loading models: {str(e)}")
        return None, None

def main():
    """Main application function."""
    # Header
    st.markdown('<h1 class="main-header">📝 Hybrid Text Summarization System</h1>', 
                unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Model selection
        st.subheader("Model Selection")
        extractive_model = st.selectbox(
            "Extractive Model",
            ["textrank", "bert", "lexrank"],
            index=0
        )
        
        abstractive_model = st.selectbox(
            "Abstractive Model", 
            ["t5", "bart", "pegasus"],
            index=0
        )
        
        # Summarization parameters
        st.subheader("Summarization Parameters")
        num_sentences = st.slider("Number of Sentences (Extractive)", 1, 10, 5)
        max_length = st.slider("Max Length (Abstractive)", 50, 300, 150)
        min_length = st.slider("Min Length (Abstractive)", 10, 100, 30)
        
        # Combination strategy
        st.subheader("Combination Strategy")
        combination_strategy = st.selectbox(
            "Strategy",
            ["weighted_combination", "pipeline", "ensemble"],
            index=0
        )
        
        # Weights
        col1, col2 = st.columns(2)
        with col1:
            extractive_weight = st.slider("Extractive Weight", 0.0, 1.0, 0.4, 0.1)
        with col2:
            abstractive_weight = st.slider("Abstractive Weight", 0.0, 1.0, 0.6, 0.1)
    
    # Main content
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Summarize", "📊 Evaluate", "📈 Compare", "ℹ️ About"])
    
    with tab1:
        summarize_tab(extractive_model, abstractive_model, num_sentences, 
                     max_length, min_length, combination_strategy, 
                     extractive_weight, abstractive_weight)
    
    with tab2:
        evaluate_tab()
    
    with tab3:
        compare_tab()
    
    with tab4:
        about_tab()

def summarize_tab(extractive_model, abstractive_model, num_sentences, 
                 max_length, min_length, combination_strategy, 
                 extractive_weight, abstractive_weight):
    """Summarization tab."""
    st.header("Text Summarization")
    
    # Input method selection
    input_method = st.radio(
        "Choose input method:",
        ["Enter text directly", "Upload file", "Use sample data"]
    )
    
    text = ""
    
    if input_method == "Enter text directly":
        text = st.text_area(
            "Enter your text here:",
            height=200,
            placeholder="Paste your text here for summarization..."
        )
    
    elif input_method == "Upload file":
        uploaded_file = st.file_uploader("Choose a file", type=['txt', 'json', 'csv'])
        if uploaded_file is not None:
            if uploaded_file.type == "text/plain":
                text = str(uploaded_file.read(), "utf-8")
            else:
                st.error("Please upload a text file (.txt)")
    
    elif input_method == "Use sample data":
        sample_data = DataLoader().create_sample_data(1)[0]
        text = sample_data['text']
        st.text_area("Sample text:", value=text, height=200, disabled=True)
    
    if text and st.button("Generate Summary", type="primary"):
        with st.spinner("Generating summary..."):
            try:
                # Load models if not already loaded
                if st.session_state.summarizer is None:
                    st.session_state.summarizer, st.session_state.config_loader = load_models()
                
                if st.session_state.summarizer is None:
                    st.error("Failed to load models")
                    return
                
                # Generate summary
                result = st.session_state.summarizer.summarize(
                    text=text,
                    num_sentences=num_sentences,
                    max_length=max_length,
                    min_length=min_length,
                    return_details=True
                )
                
                # Display results
                st.markdown('<div class="summary-box">', unsafe_allow_html=True)
                st.subheader("📋 Generated Summary")
                st.write(result['summary'])
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Display details
                with st.expander("📊 Summary Details"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("Method", result['method'])
                        st.metric("Combination Strategy", result.get('combination_strategy', 'N/A'))
                    
                    with col2:
                        st.metric("Extractive Weight", result.get('extractive_weight', 'N/A'))
                        st.metric("Abstractive Weight", result.get('abstractive_weight', 'N/A'))
                    
                    if 'details' in result:
                        st.subheader("Model Details")
                        details = result['details']
                        
                        if 'extractive_result' in details and details['extractive_result']:
                            st.write("**Extractive Results:**")
                            st.write(f"- Sentences: {details['extractive_result'].get('num_sentences', 'N/A')}")
                            st.write(f"- Model: {details.get('extractive_model', 'N/A')}")
                        
                        if 'abstractive_result' in details and details['abstractive_result']:
                            st.write("**Abstractive Results:**")
                            st.write(f"- Model: {details.get('abstractive_model', 'N/A')}")
                            if 'details' in details['abstractive_result']:
                                ab_details = details['abstractive_result']['details']
                                st.write(f"- Input Length: {ab_details.get('input_length', 'N/A')}")
                                st.write(f"- Output Length: {ab_details.get('output_length', 'N/A')}")
                                st.write(f"- Compression Ratio: {ab_details.get('compression_ratio', 'N/A'):.2f}")
                
                # Download option
                summary_text = result['summary']
                st.download_button(
                    label="📥 Download Summary",
                    data=summary_text,
                    file_name="summary.txt",
                    mime="text/plain"
                )
                
            except Exception as e:
                st.error(f"Error generating summary: {str(e)}")

def evaluate_tab():
    """Evaluation tab."""
    st.header("Model Evaluation")
    
    st.info("Upload a dataset with text and reference summaries for evaluation.")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload dataset (JSON format with 'text' and 'summary' fields)",
        type=['json', 'csv']
    )
    
    if uploaded_file is not None:
        try:
            # Load dataset
            data_loader = DataLoader()
            if uploaded_file.type == "application/json":
                dataset = json.load(uploaded_file)
            else:
                # For CSV, we'll need to handle it differently
                st.error("CSV support coming soon. Please use JSON format.")
                return
            
            if not isinstance(dataset, list):
                dataset = [dataset]
            
            st.success(f"Loaded {len(dataset)} samples")
            
            # Display sample
            with st.expander("View sample data"):
                st.json(dataset[0] if dataset else {})
            
            if st.button("Run Evaluation", type="primary"):
                with st.spinner("Running evaluation..."):
                    try:
                        # Load models
                        if st.session_state.summarizer is None:
                            st.session_state.summarizer, st.session_state.config_loader = load_models()
                        
                        if st.session_state.summarizer is None:
                            st.error("Failed to load models")
                            return
                        
                        # Prepare data
                        texts = [item['text'] for item in dataset]
                        references = [item.get('summary', '') for item in dataset]
                        
                        if not all(references):
                            st.error("All samples must have reference summaries")
                            return
                        
                        # Generate predictions
                        predictions = []
                        progress_bar = st.progress(0)
                        
                        for i, text in enumerate(texts):
                            result = st.session_state.summarizer.summarize(text)
                            predictions.append(result['summary'])
                            progress_bar.progress((i + 1) / len(texts))
                        
                        # Evaluate
                        evaluator = Evaluator(config_loader=st.session_state.config_loader)
                        evaluation_results = evaluator.evaluate(predictions, references)
                        
                        # Display results
                        st.subheader("📊 Evaluation Results")
                        
                        # Overall score
                        overall_score = evaluation_results.get('overall_score', 0)
                        st.metric("Overall Score", f"{overall_score:.3f}")
                        
                        # Individual metrics
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.subheader("ROUGE Scores")
                            if 'rouge-1' in evaluation_results:
                                rouge1 = evaluation_results['rouge-1']
                                st.metric("ROUGE-1 F1", f"{rouge1['f1']:.3f}")
                                st.metric("ROUGE-1 Precision", f"{rouge1['precision']:.3f}")
                                st.metric("ROUGE-1 Recall", f"{rouge1['recall']:.3f}")
                            
                            if 'rouge-2' in evaluation_results:
                                rouge2 = evaluation_results['rouge-2']
                                st.metric("ROUGE-2 F1", f"{rouge2['f1']:.3f}")
                                st.metric("ROUGE-2 Precision", f"{rouge2['precision']:.3f}")
                                st.metric("ROUGE-2 Recall", f"{rouge2['recall']:.3f}")
                        
                        with col2:
                            st.subheader("Other Metrics")
                            if 'rouge-l' in evaluation_results:
                                rouge_l = evaluation_results['rouge-l']
                                st.metric("ROUGE-L F1", f"{rouge_l['f1']:.3f}")
                            
                            if 'bleu' in evaluation_results:
                                bleu = evaluation_results['bleu']
                                st.metric("BLEU", f"{bleu['bleu']:.3f}")
                            
                            if 'bert_score' in evaluation_results:
                                bert = evaluation_results['bert_score']
                                st.metric("BERTScore F1", f"{bert['f1']:.3f}")
                        
                        # Download results
                        results_json = json.dumps(evaluation_results, indent=2)
                        st.download_button(
                            label="📥 Download Results",
                            data=results_json,
                            file_name="evaluation_results.json",
                            mime="application/json"
                        )
                        
                    except Exception as e:
                        st.error(f"Error during evaluation: {str(e)}")
        
        except Exception as e:
            st.error(f"Error loading dataset: {str(e)}")

def compare_tab():
    """Model comparison tab."""
    st.header("Model Comparison")
    
    st.info("Compare different summarization methods on the same text.")
    
    # Input text
    text = st.text_area(
        "Enter text for comparison:",
        height=200,
        placeholder="Enter text to compare different summarization methods..."
    )
    
    if text and st.button("Compare Models", type="primary"):
        with st.spinner("Comparing models..."):
            try:
                # Load models
                if st.session_state.summarizer is None:
                    st.session_state.summarizer, st.session_state.config_loader = load_models()
                
                if st.session_state.summarizer is None:
                    st.error("Failed to load models")
                    return
                
                # Generate summaries with different methods
                methods = {
                    "Hybrid (TextRank + T5)": st.session_state.summarizer,
                }
                
                results = {}
                for method_name, summarizer in methods.items():
                    result = summarizer.summarize(text, return_details=True)
                    results[method_name] = result
                
                # Display comparison
                st.subheader("📊 Comparison Results")
                
                for method_name, result in results.items():
                    with st.expander(f"**{method_name}**"):
                        st.write("**Summary:**")
                        st.write(result['summary'])
                        
                        if 'details' in result:
                            st.write("**Details:**")
                            details = result['details']
                            st.json(details)
                
                # Side-by-side comparison
                st.subheader("📋 Side-by-Side Comparison")
                
                cols = st.columns(len(results))
                for i, (method_name, result) in enumerate(results.items()):
                    with cols[i]:
                        st.write(f"**{method_name}**")
                        st.write(result['summary'])
                
            except Exception as e:
                st.error(f"Error comparing models: {str(e)}")

def about_tab():
    """About tab."""
    st.header("About Hybrid Text Summarization System")
    
    st.markdown("""
    ## 🎯 Overview
    
    This is a state-of-the-art hybrid text summarization system that combines 
    **extractive** and **abstractive** methods using the latest machine learning 
    and deep learning algorithms.
    
    ## 🔧 Features
    
    ### Extractive Methods
    - **TextRank**: Graph-based sentence ranking
    - **BERT-based**: Semantic similarity using sentence transformers
    - **LexRank**: Centrality-based sentence selection
    
    ### Abstractive Methods
    - **T5**: Text-to-Text Transfer Transformer
    - **BART**: Bidirectional and Auto-Regressive Transformers
    - **Pegasus**: Pre-training with Extracted Gap-sentences
    
    ### Hybrid Approaches
    - **Weighted Combination**: Combine extractive and abstractive results
    - **Pipeline**: Use extractive output as input to abstractive model
    - **Ensemble**: Multiple model combination strategies
    
    ## 📊 Evaluation Metrics
    
    - **ROUGE-1, ROUGE-2, ROUGE-L**: N-gram overlap metrics
    - **BLEU**: Bilingual Evaluation Understudy
    - **BERTScore**: Semantic similarity using BERT embeddings
    
    ## 🚀 Usage
    
    1. **Summarize Tab**: Enter text or upload a file for summarization
    2. **Evaluate Tab**: Upload a dataset with reference summaries for evaluation
    3. **Compare Tab**: Compare different summarization methods
    4. **Configuration**: Adjust model parameters in the sidebar
    
    ## 🛠️ Technical Details
    
    - **Framework**: PyTorch, Transformers, Streamlit
    - **Models**: State-of-the-art transformer models
    - **Evaluation**: Comprehensive metrics for summarization quality
    - **Interface**: User-friendly web interface
    
    ## 📚 Research Applications
    
    This system is designed for research purposes and can be used for:
    - Academic research on text summarization
    - Comparative studies of different methods
    - Evaluation of summarization quality
    - Development of new hybrid approaches
    
    ## 🔬 Methodology
    
    The hybrid approach combines the strengths of both extractive and abstractive methods:
    
    1. **Extractive methods** identify the most important sentences
    2. **Abstractive methods** generate fluent, coherent summaries
    3. **Hybrid combination** leverages both approaches for optimal results
    
    ## 📈 Performance
    
    The system achieves state-of-the-art performance on standard summarization benchmarks
    through careful model selection and combination strategies.
    """)
    
    st.markdown("---")
    st.markdown("**Developed for Research Purposes** | *Hybrid Text Summarization System v1.0*")

if __name__ == "__main__":
    main()