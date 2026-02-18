"""
Audio Processor for Synesthesia Engine

Analyzes audio chunks in real-time using Librosa to extract:
- BPM (tempo)
- Energy level
- Spectral centroid (brightness)
"""

import numpy as np
import librosa
import io
import soundfile as sf
from typing import Dict, Tuple
import logging

logger = logging.getLogger(__name__)

class AudioProcessor:
    """Real-time audio analysis for visual generation."""
    
    def __init__(self, sample_rate: int = 22050):
        """
        Initialize audio processor.
        
        Args:
            sample_rate: Audio sample rate (default 22050 Hz)
        """
        self.sample_rate = sample_rate
        self.audio_buffer = []
        
    def process_chunk(self, audio_bytes: bytes) -> Dict[str, float]:
        """
        Process a single audio chunk and extract features.
        
        Args:
            audio_bytes: Raw audio data
            
        Returns:
            Dictionary with audio features (bpm, energy, spectral_centroid)
        """
        try:
            # Convert bytes to numpy array
            audio_data, sr = self._bytes_to_audio(audio_bytes)
            
            if len(audio_data) < self.sample_rate * 0.5:  # Need at least 0.5s
                logger.warning("Audio chunk too short for analysis")
                return self._default_features()
            
            # Extract features
            bpm = self._extract_bpm(audio_data, sr)
            energy = self._calculate_energy(audio_data)
            spectral_centroid = self._calculate_spectral_centroid(audio_data, sr)
            
            features = {
                "bpm": float(bpm),
                "energy": float(energy),
                "spectral_centroid": float(spectral_centroid),
                "duration": len(audio_data) / sr
            }
            
            logger.info(f"Extracted features: {features}")
            return features
            
        except Exception as e:
            logger.error(f"Error processing audio chunk: {e}", exc_info=True)
            return self._default_features()
    
    def _bytes_to_audio(self, audio_bytes: bytes) -> Tuple[np.ndarray, int]:
        """Convert raw bytes to audio array."""
        try:
            # Try loading as WAV
            audio_data, sr = sf.read(io.BytesIO(audio_bytes))
            
            # Convert stereo to mono if needed
            if len(audio_data.shape) > 1:
                audio_data = np.mean(audio_data, axis=1)
            
            # Resample if needed
            if sr != self.sample_rate:
                audio_data = librosa.resample(
                    audio_data,
                    orig_sr=sr,
                    target_sr=self.sample_rate
                )
                sr = self.sample_rate
            
            return audio_data, sr
            
        except Exception as e:
            logger.error(f"Error converting bytes to audio: {e}")
            # Return silence if conversion fails
            return np.zeros(self.sample_rate), self.sample_rate
    
    def _extract_bpm(self, audio_data: np.ndarray, sr: int) -> float:
        """
        Extract BPM (tempo) from audio.
        
        Args:
            audio_data: Audio signal
            sr: Sample rate
            
        Returns:
            BPM value
        """
        try:
            # Use onset strength for tempo estimation
            onset_env = librosa.onset.onset_strength(y=audio_data, sr=sr)
            tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr)[0]
            
            # Clamp to reasonable range
            tempo = np.clip(tempo, 40, 200)
            
            return tempo
            
        except Exception as e:
            logger.error(f"Error extracting BPM: {e}")
            return 120.0  # Default tempo
    
    def _calculate_energy(self, audio_data: np.ndarray) -> float:
        """
        Calculate RMS energy level (normalized 0-1).
        
        Args:
            audio_data: Audio signal
            
        Returns:
            Energy level between 0 and 1
        """
        try:
            # RMS energy
            rms = librosa.feature.rms(y=audio_data)[0]
            energy = np.mean(rms)
            
            # Normalize to 0-1 range (assuming max RMS of 0.5)
            energy = np.clip(energy / 0.5, 0, 1)
            
            return energy
            
        except Exception as e:
            logger.error(f"Error calculating energy: {e}")
            return 0.5  # Medium energy
    
    def _calculate_spectral_centroid(self, audio_data: np.ndarray, sr: int) -> float:
        """
        Calculate spectral centroid (brightness).
        
        Args:
            audio_data: Audio signal
            sr: Sample rate
            
        Returns:
            Spectral centroid in Hz
        """
        try:
            centroid = librosa.feature.spectral_centroid(y=audio_data, sr=sr)[0]
            return np.mean(centroid)
            
        except Exception as e:
            logger.error(f"Error calculating spectral centroid: {e}")
            return 4000.0  # Default balanced value
    
    def _default_features(self) -> Dict[str, float]:
        """Return default features when analysis fails."""
        return {
            "bpm": 120.0,
            "energy": 0.5,
            "spectral_centroid": 4000.0,
            "duration": 0.0
        }
    
    def classify_energy_level(self, features: Dict[str, float]) -> str:
        """
        Classify energy level based on BPM and energy.
        
        Args:
            features: Audio features dictionary
            
        Returns:
            Energy classification: 'silent', 'low_energy', 'medium_energy', 'high_energy'
        """
        bpm = features.get("bpm", 120)
        energy = features.get("energy", 0.5)
        
        # Classify based on thresholds from lore_config.json
        if bpm < 40 and energy < 0.1:
            return "silent"
        elif bpm < 80 and energy < 0.4:
            return "low_energy"
        elif bpm < 120 and energy < 0.7:
            return "medium_energy"
        else:
            return "high_energy"


def map_features_to_prompt(features: Dict[str, float], lore_config: Dict) -> str:
    """
    Map audio features to Odyssey generation prompt using lore config.
    
    Args:
        features: Audio features from processor
        lore_config: Loaded lore configuration
        
    Returns:
        Odyssey-ready prompt string
    """
    # Classify energy level
    processor = AudioProcessor()
    energy_level = processor.classify_energy_level(features)
    
    # Get mapping from lore config
    mapping = lore_config["audio_mappings"].get(energy_level, {})
    
    # Extract details
    scene = mapping.get("scene_description", "Dino in cyberpunk landscape")
    camera = mapping.get("camera_movement", "smooth")
    lighting = mapping.get("lighting_style", "ambient")
    colors = mapping.get("lighting_colors", ["#00ff9f"])
    mood = mapping.get("mood", "neutral")
    effects = mapping.get("effects", [])
    
    # Get character details
    dino = lore_config["character_design"]["dino"]
    
    # Construct prompt using template
    color_str = "/".join(colors)
    effects_str = ", ".join(effects)
    
    prompt = (
        f"Cinematic shot of {dino['aesthetics']} T-Rex {scene.lower()}, "
        f"{camera} camera movement, {lighting} lighting with {color_str} palette, "
        f"{mood} atmosphere, {effects_str}, "
        f"photorealistic with cyberpunk prehistoric fusion aesthetic"
    )
    
    logger.info(f"Generated prompt for {energy_level}: {prompt}")
    return prompt
