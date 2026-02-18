"""
WHAT DI U MEAN - Speech-to-Text Engine
Uses Vosk for local, fast speech recognition
"""

import json
import os
import queue
import sounddevice as sd
import vosk
from typing import Callable, Optional
import logging

logger = logging.getLogger(__name__)


class SpeechToTextEngine:
    """Real-time speech recognition using Vosk"""
    
    def __init__(self, model_path: str = "models/vosk-model-small-en-us-0.15"):
        """
        Initialize Vosk speech recognition
        
        Args:
            model_path: Path to Vosk model directory
        """
        self.model_path = model_path
        self.model = None
        self.recognizer = None
        self.audio_queue = queue.Queue()
        self.sample_rate = 16000
        self.is_listening = False
        
        # Callback for transcription results
        self.on_transcription: Optional[Callable[[str], None]] = None
        
    def load_model(self):
        """Load Vosk model from disk"""
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(
                f"Vosk model not found at {self.model_path}. "
                f"Download from https://alphacephei.com/vosk/models"
            )
        
        logger.info(f"Loading Vosk model from {self.model_path}...")
        self.model = vosk.Model(self.model_path)
        self.recognizer = vosk.KaldiRecognizer(self.model, self.sample_rate)
        self.recognizer.SetWords(True)  # Get word timings
        logger.info("✅ Vosk model loaded successfully")
    
    def audio_callback(self, indata, frames, time_info, status):
        """Called for each audio chunk from microphone"""
        if status:
            logger.warning(f"Audio status: {status}")
        
        # Add audio data to queue
        self.audio_queue.put(bytes(indata))
    
    def start_listening(self, on_transcription: Callable[[str], None]):
        """
        Start continuous speech recognition
        
        Args:
            on_transcription: Callback function(text: str) called when speech detected
        """
        if not self.model:
            self.load_model()
        
        self.on_transcription = on_transcription
        self.is_listening = True
        
        logger.info("🎤 Starting microphone...")
        
        # Start audio stream
        with sd.RawInputStream(
            samplerate=self.sample_rate,
            blocksize=8000,  # ~500ms chunks for good responsiveness
            dtype='int16',
            channels=1,
            callback=self.audio_callback
        ):
            logger.info("✅ Listening... Speak now!")
            
            while self.is_listening:
                # Get audio chunk from queue
                try:
                    data = self.audio_queue.get(timeout=1)
                except queue.Empty:
                    continue
                
                # Process with Vosk
                if self.recognizer.AcceptWaveform(data):
                    # Final result (end of utterance)
                    result = json.loads(self.recognizer.Result())
                    text = result.get('text', '').strip()
                    
                    if text:
                        logger.info(f"📝 Heard: '{text}'")
                        if self.on_transcription:
                            self.on_transcription(text)
                else:
                    # Partial result (still speaking)
                    partial = json.loads(self.recognizer.PartialResult())
                    partial_text = partial.get('partial', '')
                    if partial_text:
                        logger.debug(f"... {partial_text}")
    
    def stop_listening(self):
        """Stop speech recognition"""
        logger.info("🛑 Stopping speech recognition")
        self.is_listening = False
    
    def transcribe_audio_file(self, audio_path: str) -> str:
        """
        Transcribe an audio file (for testing)
        
        Args:
            audio_path: Path to WAV file (16kHz, mono)
            
        Returns:
            Transcribed text
        """
        if not self.model:
            self.load_model()
        
        import wave
        
        wf = wave.open(audio_path, "rb")
        
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
            raise ValueError("Audio file must be 16kHz mono WAV")
        
        rec = vosk.KaldiRecognizer(self.model, wf.getframerate())
        
        result_text = []
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get('text', '')
                if text:
                    result_text.append(text)
        
        # Final result
        final = json.loads(rec.FinalResult())
        if final.get('text'):
            result_text.append(final['text'])
        
        return ' '.join(result_text)


if __name__ == "__main__":
    # Simple test
    logging.basicConfig(level=logging.INFO)
    
    engine = SpeechToTextEngine()
    
    def on_speech(text):
        print(f"\n🗣️  YOU SAID: {text}\n")
    
    try:
        engine.start_listening(on_speech)
    except KeyboardInterrupt:
        print("\nStopped by user")
        engine.stop_listening()
