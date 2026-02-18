"""
WHAT DI U MEAN - Test Script
Simple test to verify speech → video generation
"""

import asyncio
import sys
import os
import logging

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

from speech.stt_engine import SpeechToTextEngine
from speech.keyword_extractor import KeywordExtractor
from odyssey_client import OdysseyClient

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


class WhatDiUMean:
    """WHAT DI U MEAN - Speech-to-Visual Translator"""
    
    def __init__(self):
        self.stt = SpeechToTextEngine()
        self.extractor = KeywordExtractor()
        self.odyssey = OdysseyClient()
        
        logger.info("🎬 WHAT DI U MEAN - Ready!")
    
    async def on_speech(self, text: str):
        """Handle transcribed speech"""
        print(f"\n🗣️  YOU SAID: {text}")
        
        # Extract keywords and build prompt
        prompt = self.extractor.process_speech(text)
        print(f"🎨 VISUAL PROMPT: {prompt}")
        
        # Generate video
        try:
            print(f"⏳ Generating video...")
            result = await self.odyssey.generate_scene(prompt, portrait=True)
            job_id = result['job_id']
            print(f"✅ Video generation started! Job ID: {job_id}")
            print(f"📺 Check status at: http://localhost:8000/job/{job_id}")
            print(f"🌐 Or open playground: http://localhost:5173/playground.html")
            print()
        except Exception as e:
            logger.error(f"❌ Error generating video: {e}")
    
    async def run(self):
        """Run the speech-to-visual system"""
        print("\n" + "="*60)
        print("🎤 WHAT DI U MEAN - Speech-to-Visual Translator")
        print("="*60)
        print("\nSpeak clearly into your microphone!")
        print("Try saying:")
        print("  - 'cat'")
        print("  - 'red car'")
        print("  - 'big blue dragon'")
        print("\nPress Ctrl+C to stop\n")
        
        # Get the running event loop
        loop = asyncio.get_running_loop()
        
        def handle_speech(text):
            """Sync wrapper for async handler - schedule in event loop"""
            asyncio.run_coroutine_threadsafe(self.on_speech(text), loop)
        
        try:
            # Note: start_listening is blocking, so run in thread
            import threading
            listen_thread = threading.Thread(
                target=self.stt.start_listening,
                args=(handle_speech,),
                daemon=True  # Make daemon so it exits with main thread
            )
            listen_thread.start()
            
            # Keep main loop running
            while listen_thread.is_alive():
                await asyncio.sleep(0.1)
                
        except KeyboardInterrupt:
            print("\n\n👋 Stopping...")
            self.stt.stop_listening()


async def main():
    app = WhatDiUMean()
    await app.run()


if __name__ == "__main__":
    asyncio.run(main())
