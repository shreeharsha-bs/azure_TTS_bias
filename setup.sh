#!/bin/bash

# Azure TTS CLI Setup Script

echo "🎤 Azure Text-to-Speech CLI Setup"
echo "=================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "📋 Installing requirements..."
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Set up your Azure Speech Service credentials in .env file:"
echo "   SPEECH_KEY=your_key_here"
echo "   SPEECH_REGION=your_region_here"
echo ""
echo "2. Test the installation:"
echo "   python azure_tts_cli.py --list-voices"
echo ""
echo "3. Try a simple example:"
echo "   python azure_tts_cli.py -t 'Hello world!' --play"
echo ""
echo "For more information, see README.md"
