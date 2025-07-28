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

def simple_cbc_encrypt(plaintext, key, block_size):
    iv = os.urandom(block_size)
    text_bytes = pad(plaintext.encode(), block_size)
    blocks = split_into_blocks(text_bytes, block_size)
    
    ciphertext = b''
    previous_block = iv
    
    for block in blocks:
        # XOR with previous block (IV for first)
        xored = bytes([block[i] ^ previous_block[i] for i in range(block_size)])
        # XOR with key (simple "encryption")
        encrypted_block = bytes([xored[i] ^ key[i % len(key)] for i in range(block_size)])
        ciphertext += encrypted_block
        previous_block = encrypted_block
    
    return base64.b64encode(iv + ciphertext).decode()

def simple_cbc_decrypt(ciphertext, key, block_size):
    data = base64.b64decode(ciphertext)
    iv = data[:block_size]
    ciphertext_blocks = split_into_blocks(data[block_size:], block_size)
    
    decrypted = b''
    previous_block = iv
    
    for block in ciphertext_blocks:
        # XOR with key (simple "decryption")
        decrypted_block = bytes([block[i] ^ key[i % len(key)] for i in range(block_size)])
        # XOR with previous ciphertext block
        plain_block = bytes([decrypted_block[i] ^ previous_block[i] for i in range(block_size)])
        decrypted += plain_block
        previous_block = block
    
    return unpad(decrypted).decode()

# User inputs
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

encrypted = simple_cbc_encrypt(plaintext, key, block_size)
decrypted = simple_cbc_decrypt(encrypted, key, block_size)

print("\nSimplified CBC Mode:")
print("Original:", plaintext)
print("Encrypted (Base64):", encrypted)
print("Decrypted:", decrypted)