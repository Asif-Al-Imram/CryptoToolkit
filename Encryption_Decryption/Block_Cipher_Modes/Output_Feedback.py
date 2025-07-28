import os
import base64

def split_into_blocks(data, block_size):
    blocks = []
    i = 0
    while i < len(data):
        blocks.append(data[i:i + block_size])
        i += block_size
    return blocks

def pad(text_bytes, block_size):
    pad_len = block_size - (len(text_bytes) % block_size)
    return text_bytes + bytes([pad_len] * pad_len)

def unpad(text_bytes):
    return text_bytes[:-text_bytes[-1]]

def simple_ofb_encrypt(plaintext, key, block_size):
    iv = os.urandom(block_size)
    # Initial feedback = IV XOR key slice
    feedback = bytes([iv[i] ^ key[i % len(key)] for i in range(block_size)])
    
    plaintext_bytes = pad(plaintext.encode(), block_size)
    plaintext_blocks = split_into_blocks(plaintext_bytes, block_size)
    
    ciphertext = b''
    for block in plaintext_blocks:
        encrypted_block = bytes([block[j] ^ feedback[j] for j in range(len(block))])
        ciphertext += encrypted_block
        # Generate next feedback by XOR feedback with key slice
        feedback = bytes([feedback[j] ^ key[j % len(key)] for j in range(len(feedback))])
    
    return base64.b64encode(iv + ciphertext).decode()

def simple_ofb_decrypt(ciphertext, key, block_size):
    data = base64.b64decode(ciphertext)
    iv = data[:block_size]
    ciphertext_blocks = split_into_blocks(data[block_size:], block_size)
    
    feedback = bytes([iv[i] ^ key[i % len(key)] for i in range(block_size)])
    
    decrypted = b''
    for block in ciphertext_blocks:
        decrypted_block = bytes([block[j] ^ feedback[j] for j in range(len(block))])
        decrypted += decrypted_block
        feedback = bytes([feedback[j] ^ key[j % len(key)] for j in range(len(feedback))])
    
    return unpad(decrypted).decode()

# User input
key_input = input("Enter the key (at least block size length): ").strip()
key = key_input.encode()

while True:
    try:
        block_size = int(input("Enter block size (e.g., 8, 16, 32): "))
        if block_size <= 0 or block_size > len(key):
            print(f"Block size must be positive and <= length of key ({len(key)})")
            continue
        break
    except ValueError:
        print("Invalid input. Enter a positive integer.")

plaintext = input("Enter the plaintext message: ")

encrypted = simple_ofb_encrypt(plaintext, key, block_size)
decrypted = simple_ofb_decrypt(encrypted, key, block_size)

print("\nSimplified OFB Mode:")
print("Original:", plaintext)
print("Encrypted (Base64):", encrypted)
print("Decrypted:", decrypted)