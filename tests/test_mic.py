"""
Quick mic test - verify Vosk can hear you
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from speech.stt_engine import SpeechToTextEngine
import logging

logging.basicConfig(level=logging.INFO)

print("\n🎤 MIC TEST - Say something!\n")
print("This will print everything Vosk hears.\n")
print("Press Ctrl+C to stop\n")

stt = SpeechToTextEngine()

def on_speech(text):
    print(f"\n>>> HEARD: '{text}'\n")

try:
    stt.start_listening(on_speech)
except KeyboardInterrupt:
    print("\nStopped")
    stt.stop_listening()
