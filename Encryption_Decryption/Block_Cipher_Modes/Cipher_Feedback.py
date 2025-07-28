import os
import base64

def xor_bytes(a, b):
    result = bytearray(len(a))
    for i in range(len(a)):
        result[i] = a[i] ^ b[i]
    return bytes(result)

def split_into_blocks(data, block_size):
    blocks = []
    i = 0
    while i < len(data):
        blocks.append(data[i:i+block_size])
        i += block_size
    return blocks

def simple_cfb_encrypt(plaintext, key, block_size):
    iv = os.urandom(block_size)
    encrypted_iv = xor_bytes(iv, key[:block_size])  # XOR IV with key (key might be longer)
    
    plaintext_bytes = plaintext.encode()
    plaintext_blocks = split_into_blocks(plaintext_bytes, block_size)
    
    ciphertext = b''
    previous_block = encrypted_iv
    
    for block in plaintext_blocks:
        encrypted_block = xor_bytes(block, previous_block[:len(block)])
        ciphertext += encrypted_block
        previous_block = xor_bytes(encrypted_block, key[:len(encrypted_block)])
    
    return base64.b64encode(iv + ciphertext).decode()

def simple_cfb_decrypt(ciphertext, key, block_size):
    data = base64.b64decode(ciphertext)
    iv = data[:block_size]
    ciphertext_blocks = split_into_blocks(data[block_size:], block_size)
    
    encrypted_iv = xor_bytes(iv, key[:block_size])
    
    decrypted = b''
    previous_block = encrypted_iv
    
    for block in ciphertext_blocks:
        decrypted_block = xor_bytes(block, previous_block[:len(block)])
        decrypted += decrypted_block
        previous_block = xor_bytes(block, key[:len(block)])
    
    return decrypted.decode()

# User input
key_input = input("Enter encryption key (at least block size length): ")
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

plaintext = input("Enter plaintext to encrypt: ")

encrypted = simple_cfb_encrypt(plaintext, key, block_size)
decrypted = simple_cfb_decrypt(encrypted, key, block_size)

print("Simplified CFB Mode:")
print("Original:", plaintext)
print("Encrypted (Base64):", encrypted)
print("Decrypted:", decrypted)