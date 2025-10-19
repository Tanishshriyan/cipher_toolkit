# frequency_analyzer.py
import string
from collections import Counter
from classical_ciphers import CaesarCipher

class FrequencyAnalyzer:
    def __init__(self):
        # English letter frequencies (approximate)
        self.english_frequencies = {
            'a': 8.2, 'b': 1.5, 'c': 2.8, 'd': 4.3, 'e': 13.0,
            'f': 2.2, 'g': 2.0, 'h': 6.1, 'i': 7.0, 'j': 0.15,
            'k': 0.77, 'l': 4.0, 'm': 2.4, 'n': 6.7, 'o': 7.5,
            'p': 1.9, 'q': 0.095, 'r': 6.0, 's': 6.3, 't': 9.1,
            'u': 2.8, 'v': 0.98, 'w': 2.4, 'x': 0.15, 'y': 2.0,
            'z': 0.074
        }
    
    def analyze(self, text):
        """Calculate letter frequencies in the given text"""
        text = text.lower()
        letters = [char for char in text if char in string.ascii_lowercase]
        total_letters = len(letters)
        
        if total_letters == 0:
            return {}
        
        frequencies = {}
        for letter in string.ascii_lowercase:
            count = letters.count(letter)
            frequencies[letter] = (count / total_letters) * 100
        
        return frequencies
    
    def _calculate_word_score(self, text, common_words):
        """Calculate score based on real English words with better boundary detection"""
        words = text.lower().split()
        word_score = 0
        word_count = 0
        found_words = []
        
        for word in words:
            # Remove all non-alphabet characters for checking
            clean_word = ''.join(char for char in word if char.isalpha())
            
            if not clean_word:
                continue
                
            # Exact match gets highest score
            if clean_word in common_words:
                word_score += 20
                word_count += 1
                found_words.append(clean_word)
                continue
                
            # Check for common word endings/prefixes
            base_word = clean_word
            
            # Try removing common suffixes
            suffixes = ['s', 'ed', 'ing', 'ly', 'er', 'est', 'ment', 'ness']
            for suffix in suffixes:
                if (len(base_word) > len(suffix) + 2 and 
                    base_word.endswith(suffix) and 
                    base_word[:-len(suffix)] in common_words):
                    word_score += 15
                    word_count += 1
                    found_words.append(base_word[:-len(suffix)])
                    break
            else:  # If no suffix matched, try partial matches
                # Check if word starts or ends with common words
                for common in common_words:
                    if len(common) > 3:
                        if clean_word.startswith(common):
                            word_score += 10
                            break
                        elif clean_word.endswith(common):
                            word_score += 10
                            break
        
        return word_score, word_count, found_words
    
    def crack_caesar(self, ciphertext):
        """Try all possible Caesar shifts and return the most likely plaintext"""
        best_shift = 0
        best_score = float('inf')
        best_plaintext = ""
        
        # Common English words for dictionary scoring
        common_words = {
            # Common short words
            'a', 'i', 'be', 'to', 'of', 'in', 'it', 'on', 'he', 'we', 'me', 'us',
            'is', 'am', 'are', 'was', 'were', 'be', 'being', 'been',
            
            # Pronouns
            'you', 'your', 'yours', 'he', 'him', 'his', 'she', 'her', 'hers', 
            'they', 'them', 'their', 'theirs', 'we', 'our', 'ours', 'i', 'my', 'mine',
            
            # Common verbs
            'have', 'has', 'had', 'do', 'does', 'did', 'say', 'says', 'said',
            'get', 'got', 'make', 'made', 'go', 'went', 'gone', 'know', 'knew',
            'see', 'saw', 'come', 'came', 'think', 'thought', 'look', 'looked',
            'want', 'wanted', 'give', 'gave', 'use', 'used', 'find', 'found',
            'tell', 'told', 'ask', 'asked', 'work', 'worked', 'seem', 'seemed',
            'feel', 'felt', 'try', 'tried', 'leave', 'left', 'call', 'called',
            'break', 'broke', 'broken', 'reset', 'set',
            
            # Common nouns
            'time', 'person', 'year', 'way', 'day', 'thing', 'man', 'world',
            'life', 'hand', 'part', 'child', 'eye', 'woman', 'place', 'work',
            'week', 'case', 'point', 'company', 'number', 'group', 'problem',
            'fact', 'password', 'daily', 'second', 'first',
            
            # Common adjectives/adverbs
            'good', 'new', 'first', 'last', 'long', 'great', 'little', 'own',
            'other', 'old', 'right', 'big', 'high', 'different', 'small',
            'large', 'next', 'early', 'young', 'important', 'few', 'public',
            
            # Special words for our context
            'hello', 'world', 'the', 'quick', 'brown', 'fox', 'jumps', 'over',
            'lazy', 'dog'
        }
        
        print("\n=== Debug: Top 3 Candidates ===")
        scores = []
        
        for shift in range(26):
            cipher = CaesarCipher(shift)
            attempted_plaintext = cipher.decrypt(ciphertext)
            freq = self.analyze(attempted_plaintext)
            
            # Calculate frequency score
            freq_score = 0
            for letter, freq_val in freq.items():
                freq_score += abs(freq_val - self.english_frequencies.get(letter, 0))
            
            # Calculate dictionary score with improved detection
            word_score, word_count, found_words = self._calculate_word_score(attempted_plaintext, common_words)
            
            # Combined score (frequency score minus word bonuses)
            total_score = freq_score - word_score
            
            scores.append((total_score, shift, attempted_plaintext, word_score, word_count, found_words))
            
            if total_score < best_score:
                best_score = total_score
                best_shift = shift
                best_plaintext = attempted_plaintext
        
        # Show top 3 candidates with more details
        scores.sort()
        for i, (score, shift, text, word_bonus, word_count, found_words) in enumerate(scores[:3]):
            print(f"#{i+1}: Shift {shift} (score: {score:.2f}, words: {word_count}): {text}")
            if found_words:
                print(f"   Found words: {', '.join(found_words)}")
        print()
        
        return best_plaintext, best_shift