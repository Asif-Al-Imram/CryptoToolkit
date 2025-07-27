# CFC mode (simplified version)-----------------------------------------------------------------
import os
import base64

def simple_cbc_encrypt(plaintext, key):
    # Generate random IV (16 bytes)
    iv = os.urandom(16)
    
    # Pad plaintext to multiple of 16 bytes
    padding_length = 16 - (len(plaintext) % 16)
    padded_text = plaintext.encode() + bytes([padding_length] * padding_length)
    
    # Split into blocks
    blocks = [padded_text[i:i+16] for i in range(0, len(padded_text), 16)]
    
    # Encrypt each block
    ciphertext = b''
    previous_block = iv
    for block in blocks:
        # XOR with previous ciphertext block (or IV for first block)
        xored = bytes([block[i] ^ previous_block[i] for i in range(16)])
        # "Encrypt" with simple XOR (in real AES this would be complex)
        encrypted_block = bytes([xored[i] ^ key[i % len(key)] for i in range(16)])
        ciphertext += encrypted_block
        previous_block = encrypted_block
    
    return base64.b64encode(iv + ciphertext).decode()

def simple_cbc_decrypt(ciphertext, key):
    data = base64.b64decode(ciphertext)
    iv = data[:16]
    ciphertext_blocks = [data[i:i+16] for i in range(16, len(data), 16)]
    
    decrypted = b''
    previous_block = iv
    for block in ciphertext_blocks:
        # "Decrypt" with simple XOR
        decrypted_block = bytes([block[i] ^ key[i % len(key)] for i in range(16)])
        # XOR with previous ciphertext block
        plain_block = bytes([decrypted_block[i] ^ previous_block[i] for i in range(16)])
        decrypted += plain_block
        previous_block = block
    
    # Remove padding
    padding_length = decrypted[-1]
    return decrypted[:-padding_length].decode()

# Taking input from user
plaintext = input("Enter the plaintext message: ")
key_input = input("Enter the key (16 characters): ")

if len(key_input) != 16:
    print("Error: Key must be exactly 16 characters long.")
    exit(1)

key = key_input.encode()

encrypted = simple_cbc_encrypt(plaintext, key)
decrypted = simple_cbc_decrypt(encrypted, key)

print(f"Simplified CBC Mode:")
print(f"Original: {plaintext}")
print(f"Encrypted: {encrypted}")
print(f"Decrypted: {decrypted}\n")
