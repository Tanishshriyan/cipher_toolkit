# test.py
from classical_ciphers import CaesarCipher, VigenereCipher
from frequency_analyzer import FrequencyAnalyzer

print("=== Testing Classical Cipher Toolkit ===\n")

# Test Caesar Cipher
print("1. Testing Caesar Cipher:")
caesar = CaesarCipher(3)
encrypted = caesar.encrypt("HELLO WORLD")
print(f"   Encrypted: {encrypted}")
print(f"   Decrypted: {caesar.decrypt(encrypted)}")

# Test Vigenère Cipher
print("\n2. Testing Vigenère Cipher:")
vigenere = VigenereCipher("KEY")
encrypted = vigenere.encrypt("ATTACK AT DAWN")
print(f"   Encrypted: {encrypted}")
print(f"   Decrypted: {vigenere.decrypt(encrypted)}")

# Test Frequency Analysis
print("\n3. Testing Frequency Analysis Cracker:")
analyzer = FrequencyAnalyzer()

# Use a longer text for better frequency analysis
test_cipher = CaesarCipher(3)
ciphertext = test_cipher.encrypt("THIS IS A SECRET MESSAGE THAT SHOULD BE LONG ENOUGH FOR FREQUENCY ANALYSIS TO WORK PROPERLY")
print(f"   Original: THIS IS A SECRET MESSAGE...")
print(f"   Encrypted: {ciphertext}")

plaintext, shift = analyzer.crack_caesar(ciphertext)
print(f"   Cracked with shift {shift}: {plaintext[:50]}...")

# Test with a known simple ciphertext
print("\n4. Testing with known ciphertext:")
simple_ciphertext = "WKLV LV D VHFUHW PHVVDJH"
plaintext, shift = analyzer.crack_caesar(simple_ciphertext)
print(f"   Ciphertext: {simple_ciphertext}")
print(f"   Cracked with shift {shift}: {plaintext}")

print("\n=== All tests completed ===")