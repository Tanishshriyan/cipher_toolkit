# main.py
from classical_ciphers import CaesarCipher, VigenereCipher
from frequency_analyzer import FrequencyAnalyzer

def main():
    analyzer = FrequencyAnalyzer()
    
    while True:
        print("\n=== Classical Cipher Toolkit ===")
        print("1. Caesar Cipher")
        print("2. Vigenère Cipher")
        print("3. Crack Caesar Cipher (Frequency Analysis)")
        print("4. Exit")
        
        choice = input("\nSelect an option (1-4): ")
        
        if choice == '1':
            # Caesar Cipher
            text = input("Enter text: ")
            shift = int(input("Enter shift value: "))
            action = input("Encrypt or Decrypt? (e/d): ").lower()
            
            cipher = CaesarCipher(shift)
            if action == 'e':
                result = cipher.encrypt(text)
                print(f"Encrypted: {result}")
            else:
                result = cipher.decrypt(text)
                print(f"Decrypted: {result}")
        
        elif choice == '2':
            # Vigenère Cipher
            text = input("Enter text: ")
            key = input("Enter key: ")
            action = input("Encrypt or Decrypt? (e/d): ").lower()
            
            cipher = VigenereCipher(key)
            if action == 'e':
                result = cipher.encrypt(text)
                print(f"Encrypted: {result}")
            else:
                result = cipher.decrypt(text)
                print(f"Decrypted: {result}")
        
        elif choice == '3':
            # Crack Caesar Cipher
            ciphertext = input("Enter ciphertext to crack: ")
            plaintext, shift = analyzer.crack_caesar(ciphertext)
            print(f"Most likely plaintext (shift {shift}): {plaintext}")
            
            # Show frequency analysis
            print("\nFrequency Analysis:")
            freq = analyzer.analyze(ciphertext)
            for letter, percentage in sorted(freq.items()):
                print(f"{letter}: {percentage:.2f}%")
        
        elif choice == '4':
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()