#!/usr/bin/env python3
"""
Azure Text-to-Speech CLI Tool

A command-line interface for Azure Cognitive Services Text-to-Speech.
Supports generating audio from text input with customizable voice selection.
"""

import os
import sys
import argparse
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
load_dotenv()


class AzureTTSError(Exception):
    """Custom exception for Azure TTS errors."""
    pass


class AzureTTS:
    """Azure Text-to-Speech handler class."""
    
    # Popular voice options
    POPULAR_VOICES = {
        "ava": "en-US-AvaNeural",
        "andrew": "en-US-AndrewMultilingualNeural", 
        "emma": "en-US-EmmaMultilingualNeural",
        "brian": "en-US-BrianMultilingualNeural",
        "sarah": "en-US-SaraNeural",
        "christopher": "en-US-ChristopherNeural"
    }
    
    def __init__(self, voice_name=None):
        """Initialize Azure TTS with configuration."""
        self.speech_key = os.environ.get('SPEECH_KEY')
        self.region = os.environ.get('SPEECH_REGION')
        
        if not self.speech_key or not self.region:
            raise AzureTTSError(
                "SPEECH_KEY and SPEECH_REGION environment variables are required. "
                "Please set them in your .env file or environment."
            )
        
        # Set voice name
        if voice_name and voice_name.lower() in self.POPULAR_VOICES:
            self.voice_name = self.POPULAR_VOICES[voice_name.lower()]
        elif voice_name:
            self.voice_name = voice_name
        else:
            self.voice_name = os.environ.get('VOICE_NAME', 'en-US-AvaNeural')
        
        # Configure speech service
        endpoint_url = f"https://{self.region}.api.cognitive.microsoft.com/sts/v1.0/issuetoken"
        self.speech_config = speechsdk.SpeechConfig(
            subscription=self.speech_key, 
            endpoint=endpoint_url
        )
        self.speech_config.speech_synthesis_voice_name = self.voice_name
    
    def synthesize_to_file(self, text, output_file):
        """Synthesize text to audio file."""
        try:
            audio_config = speechsdk.audio.AudioOutputConfig(filename=str(output_file))
            synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=self.speech_config, 
                audio_config=audio_config
            )
            
            result = synthesizer.speak_text_async(text).get()
            
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                return True
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = result.cancellation_details
                error_msg = f"Speech synthesis canceled: {cancellation_details.reason}"
                if cancellation_details.error_details:
                    error_msg += f"\nError details: {cancellation_details.error_details}"
                raise AzureTTSError(error_msg)
            
        except Exception as e:
            raise AzureTTSError(f"Synthesis failed: {str(e)}")
        
        return False
    
    def synthesize_to_speaker(self, text):
        """Synthesize text to default speaker."""
        try:
            audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
            synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=self.speech_config, 
                audio_config=audio_config
            )
            
            result = synthesizer.speak_text_async(text).get()
            
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                return True
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = result.cancellation_details
                error_msg = f"Speech synthesis canceled: {cancellation_details.reason}"
                if cancellation_details.error_details:
                    error_msg += f"\nError details: {cancellation_details.error_details}"
                raise AzureTTSError(error_msg)
            
        except Exception as e:
            raise AzureTTSError(f"Synthesis failed: {str(e)}")
        
        return False


def read_text_file(file_path):
    """Read text from file and return lines."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
        return lines
    except FileNotFoundError:
        raise AzureTTSError(f"Text file not found: {file_path}")
    except Exception as e:
        raise AzureTTSError(f"Error reading text file: {str(e)}")


def create_output_filename(base_name, line_number, output_dir):
    """Create output filename for audio file."""
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    return output_dir / f"{base_name}_{line_number:03d}.wav"


def list_voices():
    """List available voice options."""
    print("\nPopular Voice Options:")
    print("=" * 50)
    for key, voice in AzureTTS.POPULAR_VOICES.items():
        print(f"{key:10} -> {voice}")
    print("\nFor complete list, visit:")
    print("https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/language-support#neural-voices")


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Azure Text-to-Speech CLI Tool",
        epilog="Examples:\n"
               "  %(prog)s -t 'Hello world' -o output.wav\n"
               "  %(prog)s -f sentences.txt -v emma -d ./audio_output\n"
               "  %(prog)s --list-voices\n",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Input options
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        '-t', '--text',
        help='Text to synthesize'
    )
    input_group.add_argument(
        '-f', '--file',
        help='Text file containing sentences (one per line)'
    )
    input_group.add_argument(
        '--list-voices',
        action='store_true',
        help='List available voice options'
    )
    
    # Voice selection
    parser.add_argument(
        '-v', '--voice',
        default='ava',
        help='Voice name (use popular name like "ava" or full Azure voice name). Default: ava'
    )
    
    # Output options
    parser.add_argument(
        '-o', '--output',
        help='Output audio file (for single text synthesis)'
    )
    parser.add_argument(
        '-d', '--output-dir',
        default='./output',
        help='Output directory for multiple files. Default: ./output'
    )
    parser.add_argument(
        '--prefix',
        default='tts',
        help='Filename prefix for multiple files. Default: voice name (e.g., ava, emma)'
    )
    
    # Other options
    parser.add_argument(
        '--play',
        action='store_true',
        help='Play audio through default speaker instead of saving to file'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # Handle list voices
    if args.list_voices:
        list_voices()
        return 0
    
    try:
        # Initialize Azure TTS
        if args.verbose:
            print(f"Initializing Azure TTS with voice: {args.voice}")
        
        tts = AzureTTS(voice_name=args.voice)
        
        # Set prefix to voice shortcut if not explicitly provided
        if args.prefix == 'tts':  # Default prefix value
            # Check if the voice is a shortcut name
            voice_shortcut = args.voice.lower()
            if voice_shortcut in AzureTTS.POPULAR_VOICES:
                args.prefix = voice_shortcut
            else:
                # For full voice names, extract a meaningful prefix
                if 'en-US-' in args.voice:
                    # Extract voice name from full Azure voice name
                    voice_part = args.voice.replace('en-US-', '').replace('Neural', '').replace('Multilingual', '')
                    args.prefix = voice_part.lower()
                else:
                    args.prefix = 'tts'  # Keep default for unknown formats
        
        if args.verbose:
            print(f"Using Azure voice: {tts.voice_name}")
        
        # Handle single text synthesis
        if args.text:
            if args.play:
                if args.verbose:
                    print(f"Playing text: {args.text}")
                tts.synthesize_to_speaker(args.text)
                print("✓ Audio played successfully")
            else:
                output_file = args.output or 'output.wav'
                if args.verbose:
                    print(f"Synthesizing to file: {output_file}")
                tts.synthesize_to_file(args.text, output_file)
                print(f"✓ Audio saved to: {output_file}")
        
        # Handle file input
        elif args.file:
            lines = read_text_file(args.file)
            
            if not lines:
                print("No text found in file")
                return 1
            
            print(f"Processing {len(lines)} lines from {args.file}")
            
            if args.play:
                # Play each line
                for i, line in enumerate(lines, 1):
                    if args.verbose:
                        print(f"Playing line {i}: {line[:50]}...")
                    tts.synthesize_to_speaker(line)
                    print(f"✓ Played line {i}")
            else:
                # Save each line to separate file
                for i, line in enumerate(lines, 1):
                    output_file = create_output_filename(args.prefix, i, args.output_dir)
                    
                    if args.verbose:
                        print(f"Synthesizing line {i} to: {output_file}")
                    
                    tts.synthesize_to_file(line, output_file)
                    print(f"✓ Saved line {i} to: {output_file}")
                
                print(f"\n✓ All {len(lines)} audio files saved to: {args.output_dir}")
    
    except AzureTTSError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
