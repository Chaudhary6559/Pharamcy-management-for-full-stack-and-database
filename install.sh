#!/bin/bash

# Hybrid Text Summarization System Installation Script

echo "🚀 Installing Hybrid Text Summarization System"
echo "=============================================="

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" = "$required_version" ]; then
    echo "✅ Python version $python_version is compatible"
else
    echo "❌ Python version $python_version is not compatible. Required: $required_version or higher"
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📚 Installing requirements..."
pip install -r requirements.txt

# Download NLTK data
echo "📥 Downloading NLTK data..."
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger'); nltk.download('wordnet')"

# Download SpaCy model
echo "📥 Downloading SpaCy model..."
python -m spacy download en_core_web_sm

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data/{raw,processed}
mkdir -p outputs
mkdir -p logs
mkdir -p tests

# Run tests
echo "🧪 Running tests..."
python -m pytest tests/ -v

echo ""
echo "✅ Installation completed successfully!"
echo ""
echo "🚀 To get started:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Run basic example: python examples/basic_usage.py"
echo "3. Launch web interface: streamlit run streamlit_app.py"
echo "4. Use CLI: python -m src.cli.main --help"
echo ""
echo "📚 For more information, see README.md"