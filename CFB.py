import os
import base64

def simple_cfb_encrypt(plaintext, key):
    iv = os.urandom(16)
    cipher = bytes([iv[i] ^ key[i % len(key)] for i in range(16)])  # "Encrypt" IV
    
    ciphertext = b''
    previous_block = cipher
    for i in range(0, len(plaintext), 16):
        block = plaintext.encode()[i:i+16]
        # XOR plaintext with encrypted previous block
        encrypted_block = bytes([block[j] ^ previous_block[j] for j in range(len(block))])
        ciphertext += encrypted_block
        # Next block uses current ciphertext as input
        previous_block = bytes([encrypted_block[j] ^ key[j % len(key)] for j in range(len(encrypted_block))])
    
    return base64.b64encode(iv + ciphertext).decode()

def simple_cfb_decrypt(ciphertext, key):
    data = base64.b64decode(ciphertext)
    iv = data[:16]
    ciphertext_blocks = data[16:]
    
    decrypted = b''
    previous_block = bytes([iv[i] ^ key[i % len(key)] for i in range(16)])
    for i in range(0, len(ciphertext_blocks), 16):
        block = ciphertext_blocks[i:i+16]
        # XOR ciphertext with encrypted previous block
        decrypted_block = bytes([block[j] ^ previous_block[j] for j in range(len(block))])
        decrypted += decrypted_block
        # Next block uses current ciphertext as input
        previous_block = bytes([block[j] ^ key[j % len(key)] for j in range(len(block))])
    
    return decrypted.decode()

# Taking inputs from user
plaintext = input("Enter the plaintext message: ")
key_input = input("Enter the key (16 characters): ")

# Make sure key is 16 bytes exactly
if len(key_input) != 16:
    print("Error: Key must be exactly 16 characters long.")
    exit(1)

key = key_input.encode()

encrypted = simple_cfb_encrypt(plaintext, key)
decrypted = simple_cfb_decrypt(encrypted, key)

print(f"Simplified CFB Mode:")
print(f"Original: {plaintext}")
print(f"Encrypted: {encrypted}")
print(f"Decrypted: {decrypted}")
