# Azure Text-to-Speech CLI Tool

A command-line interface for Azure Cognitive Services Text-to-Speech that allows you to convert text to speech with customizable voice selection.

## Features

- 🎤 Multiple voice options with easy-to-remember aliases
- 📄 Batch processing from text files
- 🔊 Direct audio playback or file output
- 🌍 Support for multiple languages and accents
- ⚙️ Environment-based configuration
- 📋 Command-line interface with comprehensive options

## Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Set up your Azure Speech Service credentials (see Configuration section)

## Configuration

### Azure Speech Service Setup

1. Create an Azure Speech Service resource in the [Azure Portal](https://portal.azure.com/)
2. Get your Speech Key and Region from the resource

### Environment Variables

Create a `.env` file in the project directory with your Azure credentials:

```env
SPEECH_KEY=your_speech_service_key_here
SPEECH_REGION=your_region_here
VOICE_NAME=en-US-AvaMultilingualNeural
```

**Important**: Never commit your `.env` file to version control. It contains sensitive credentials.

## Usage

### Basic Usage

```bash
# Synthesize single text to file
python azure_tts_cli.py -t "Hello, world!" -o hello.wav

# Play text through speakers
python azure_tts_cli.py -t "Hello, world!" --play

# Use different voice
python azure_tts_cli.py -t "Hello, world!" -v emma -o hello_emma.wav
```

### Batch Processing

```bash
# Process text file with multiple sentences
python azure_tts_cli.py -f sentences.txt -d ./audio_output

# Use custom prefix for output files
python azure_tts_cli.py -f sentences.txt --prefix "speech" -d ./output
```

### Voice Options

```bash
# List available voice shortcuts
python azure_tts_cli.py --list-voices

# Use voice shortcut
python azure_tts_cli.py -t "Hello" -v jenny

# Use full Azure voice name
python azure_tts_cli.py -t "Hello" -v "en-GB-SoniaNeural"
```

## Command-Line Options

### Input Options
- `-t, --text TEXT`: Text to synthesize
- `-f, --file FILE`: Text file containing sentences (one per line)
- `--list-voices`: List available voice options

### Voice Selection
- `-v, --voice VOICE`: Voice name (default: ava)
  - Use shortcuts like: ava, emma, jenny, brian, sonia, etc.
  - Or full Azure voice names like: en-US-AvaMultilingualNeural

### Output Options
- `-o, --output FILE`: Output audio file (for single text)
- `-d, --output-dir DIR`: Output directory for multiple files (default: ./output)
- `--prefix PREFIX`: Filename prefix for multiple files (default: tts)
- `--play`: Play audio through speakers instead of saving

### Other Options
- `--verbose`: Enable verbose output
- `-h, --help`: Show help message

## Available Voice Shortcuts

| Shortcut | Full Voice Name | Language/Accent |
|----------|----------------|-----------------|
| ava | en-US-AvaMultilingualNeural | US English (Multilingual) |
| andrew | en-US-AndrewMultilingualNeural | US English (Multilingual) |
| emma | en-US-EmmaMultilingualNeural | US English (Multilingual) |
| brian | en-US-BrianMultilingualNeural | US English (Multilingual) |
| jenny | en-US-JennyMultilingualNeural | US English (Multilingual) |
| sonia | en-GB-SoniaNeural | UK English |
| natasha | en-AU-NatashaNeural | Australian English |
| alvaro | es-ES-AlvaroNeural | Spanish |
| denise | fr-FR-DeniseNeural | French |
| katja | de-DE-KatjaNeural | German |
| nanami | ja-JP-NanamiNeural | Japanese |

## Text File Format

For batch processing, create a text file with one sentence per line:

```
This is the first sentence.
This is the second sentence.
And this is the third sentence.
```

Empty lines are automatically skipped.

## Examples

### Example 1: Single Text Synthesis
```bash
python azure_tts_cli.py -t "Welcome to Azure Text-to-Speech!" -v ava -o welcome.wav
```

### Example 2: Batch Processing
```bash
# Create a text file
echo -e "Hello world!\nHow are you today?\nHave a great day!" > greetings.txt

# Process the file
python azure_tts_cli.py -f greetings.txt -v emma -d ./greetings_audio --prefix greeting
```

This will create:
- `greetings_audio/greeting_001.wav`
- `greetings_audio/greeting_002.wav` 
- `greetings_audio/greeting_003.wav`

### Example 3: Interactive Playback
```bash
python azure_tts_cli.py -f announcements.txt -v brian --play --verbose
```

## Error Handling

The tool provides clear error messages for common issues:

- Missing Azure credentials
- Invalid voice names
- File not found errors
- Azure service errors

## Requirements

- Python 3.7+
- Azure Speech Service subscription
- Internet connection for Azure API calls

## Dependencies

See `requirements.txt` for the complete list of Python dependencies:

- `azure-cognitiveservices-speech`: Azure Speech SDK
- `python-dotenv`: Environment variable management

## License

This project is open source. Please check the license file for details.

## Contributing

Contributions are welcome! Please feel free to submit issues and enhancement requests.

## Support

For Azure Speech Service documentation and support:
- [Azure Speech Service Documentation](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/)
- [Neural Voice Language Support](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/language-support#neural-voices)

## Security Notes

- Never commit your `.env` file or expose your Azure Speech Service credentials
- Use environment variables or secure credential management in production
- The `.gitignore` file is configured to exclude sensitive files
