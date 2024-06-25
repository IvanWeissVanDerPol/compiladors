import json
import re

class Tokenizer:
    def __init__(self, positive_words, negative_words, neutral_words):
        self.positive_words = positive_words
        self.negative_words = negative_words
        self.neutral_words = neutral_words

    @classmethod
    def from_json(cls, json_file_path):
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return cls(
            positive_words=data['BUENAS'],
            negative_words=data['MALAS'],
            neutral_words=data['NEUTRAS']
        )

    def normalize_word(self, original_word):
        # Normalize word to handle number and gender variations
        updated_word = original_word.lower()
        if updated_word.isdigit():
            return 'neutral_number'  # Special token for numbers
        if updated_word.endswith('s'):
            updated_word = updated_word[:-1]  # Remove plural 's'
        if updated_word.endswith('a'):
            updated_word = updated_word[:-1] + 'o'  # Convert feminine to masculine
        return updated_word

    def tokenize(self, text):
        # Improved tokenization to handle punctuation and special characters
        tokens = re.findall(r'\b\w+\b', text.lower())
        return [self.normalize_word(token) for token in tokens]

    def evaluate(self, tokens):
        positive_count = sum(1 for token in tokens if token in self.positive_words)
        negative_count = sum(1 for token in tokens if token in self.negative_words)
        neutral_count = sum(1 for token in tokens if token in self.neutral_words)
        
        return {
            'positive': positive_count,
            'negative': negative_count,
            'neutral': neutral_count
        }