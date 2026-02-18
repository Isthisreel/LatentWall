"""
WHAT DI U MEAN - Keyword Extractor
Extract nouns, adjectives, verbs from speech for visual prompts
"""

import json
import os
import re
from typing import List, Tuple, Dict
import logging

logger = logging.getLogger(__name__)


class KeywordExtractor:
    """Extract keywords from transcribed speech"""
    
    def __init__(self, dictionary_path: str = "prompts/dictionary.json"):
        """
        Initialize keyword extractor
        
        Args:
            dictionary_path: Path to prompt dictionary JSON
        """
        self.dictionary_path = dictionary_path
        self.dictionary = self._load_dictionary()
        
        # Simple word lists (no NLP needed for MVP)
        self.known_words = set()
        for category in self.dictionary.values():
            self.known_words.update(category.keys())
        
        logger.info(f"✅ Loaded {len(self.known_words)} known words")
    
    def _load_dictionary(self) -> Dict:
        """Load prompt dictionary from JSON"""
        dict_path = os.path.join(os.path.dirname(__file__), "..", self.dictionary_path)
        
        with open(dict_path, 'r') as f:
            dictionary = json.load(f)
        
        return dictionary
    
    def extract_keywords(self, text: str) -> List[Tuple[str, str]]:
        """
        Extract keywords from text (simple version - no spaCy)
        
        Args:
            text: Transcribed speech
            
        Returns:
            List of (word, category) tuples
            Example: [("red", "adjectives"), ("car", "nouns")]
        """
        # Normalize text
        text = text.lower().strip()
        words = re.findall(r'\b\w+\b', text)
        
        keywords = []
        seen = set()  # Avoid duplicates
        
        for word in words:
            if word in seen:
                continue
            
            # Check which category this word belongs to
            for category, word_dict in self.dictionary.items():
                if word in word_dict:
                    keywords.append((word, category))
                    seen.add(word)
                    break
        
        logger.info(f"Extracted {len(keywords)} keywords: {keywords}")
        return keywords
    
    def build_prompt(self, keywords: List[Tuple[str, str]]) -> str:
        """
        Build visual prompt from keywords
        
        Args:
            keywords: List of (word, category) tuples
            
        Returns:
            Assembled prompt for Odyssey
        """
        if not keywords:
            return "abstract shapes and colors"
        
        # Separate by category
        nouns = []
        adjectives = []
        verbs = []
        
        for word, category in keywords:
            prompt_fragment = self.dictionary[category][word]
            
            if category == "nouns":
                nouns.append(prompt_fragment)
            elif category == "adjectives":
                adjectives.append(prompt_fragment)
            elif category == "verbs":
                verbs.append(prompt_fragment)
        
        # Assemble prompt: adjectives + nouns + verbs
        parts = []
        
        if adjectives:
            parts.extend(adjectives)
        
        if nouns:
            parts.extend(nouns)
        
        if verbs:
            parts.extend(verbs)
        
        prompt = ", ".join(parts)
        logger.info(f"Built prompt: '{prompt}'")
        
        return prompt
    
    def process_speech(self, text: str) -> str:
        """
        Full pipeline: text → keywords → prompt
        
        Args:
            text: Transcribed speech
            
        Returns:
            Visual prompt for Odyssey
        """
        keywords = self.extract_keywords(text)
        prompt = self.build_prompt(keywords)
        return prompt


if __name__ == "__main__":
    # Test
    logging.basicConfig(level=logging.INFO)
    
    extractor = KeywordExtractor()
    
    test_phrases = [
        "cat",
        "red car",
        "big blue dragon flying",
        "a scary dark forest",
        "happy yellow bird",
    ]
    
    print("\n🧪 Testing Keyword Extraction:\n")
    for phrase in test_phrases:
        prompt = extractor.process_speech(phrase)
        print(f"  '{phrase}' → '{prompt}'")
    
    print()
