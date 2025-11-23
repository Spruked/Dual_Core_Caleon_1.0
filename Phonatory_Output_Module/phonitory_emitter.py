"""
Phonitory Output Module: Basic symbolic-to-voice emitter using Coqui TTS
"""
import json
import os
from TTS.api import TTS
import sounddevice as sd
import soundfile as sf
import sys

# Import seed reference for tone consistency
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'reference_seed'))
from seed_loader import get_seed

def emit_voice(symbolic_payload: dict, save_path: str = None, play_audio: bool = True) -> str:
    """
    Converts symbolic payload (from cochlear processor) to speech audio.
    Retrieves articulation_reference from seed to maintain tone consistency.

    Args:
        symbolic_payload: dict containing at least 'symbol' (text to vocalize)
        save_path: optional file path to store the output .wav
        play_audio: if True, auto-play the generated audio

    Returns:
        Path to the generated audio file
    """
    # Retrieve articulation reference from seed for tone consistency
    articulation_reference = get_seed()
    if articulation_reference:
        behavioral_core = articulation_reference.get('behavioral_core', {})
        symbolic_tone = behavioral_core.get('symbolic_tone', [])
        # Apply tone bias to the payload
        if 'calm_groundedness' in symbolic_tone:
            symbolic_payload['tone_modifier'] = 'calm'
        elif 'precision' in symbolic_tone:
            symbolic_payload['tone_modifier'] = 'precise'
    
    # Load config
    config_path = os.path.join(os.path.dirname(__file__), 'voice_config.json')
    with open(config_path, 'r') as f:
        config = json.load(f)

    text = symbolic_payload.get('symbol', '')
    if not text:
        raise ValueError("symbolic_payload must contain a 'symbol' key with text to vocalize.")

    # Initialize TTS
    tts = TTS(model_name=config['voice_id'], progress_bar=False, gpu=False)

    # Synthesize speech
    output_path = save_path or 'output.wav'
    tts.tts_to_file(text=text, file_path=output_path)

    # Play audio if requested
    if play_audio:
        data, samplerate = sf.read(output_path)
        sd.play(data, samplerate)
        sd.wait()

    return os.path.abspath(output_path)

# Example usage:
# emit_voice({'symbol': 'Hello, world!'}, save_path='test.wav', play_audio=True)
