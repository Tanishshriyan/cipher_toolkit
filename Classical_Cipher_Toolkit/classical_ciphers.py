# classical_ciphers.py

class CaesarCipher:
    def __init__(self, shift=3):
        self.shift = shift
    
    def encrypt(self, text):
        result = ""
        for char in text:
            if char.isalpha():
                ascii_offset = 65 if char.isupper() else 97
                result += chr((ord(char) - ascii_offset + self.shift) % 26 + ascii_offset)
            else:
                result += char
        return result
    
    def decrypt(self, text):
        result = ""
        for char in text:
            if char.isalpha():
                ascii_offset = 65 if char.isupper() else 97
                result += chr((ord(char) - ascii_offset - self.shift) % 26 + ascii_offset)
            else:
                result += char
        return result

class VigenereCipher:
    def __init__(self, key):
        self.key = key.upper()
    
    def _process_text(self, text, mode='encrypt'):
        result = ""
        key_index = 0
        
        for char in text:
            if char.isalpha():
                ascii_offset = 65 if char.isupper() else 97
                key_char = self.key[key_index % len(self.key)]
                key_shift = ord(key_char) - 65
                
                if mode == 'decrypt':
                    key_shift = -key_shift
                
                result += chr((ord(char) - ascii_offset + key_shift) % 26 + ascii_offset)
                key_index += 1
            else:
                result += char
        return result
    
    def encrypt(self, text):
        return self._process_text(text, 'encrypt')
    
    def decrypt(self, text):
        return self._process_text(text, 'decrypt')