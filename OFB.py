import os
import base64

def simple_ofb_encrypt(plaintext, key):
    iv = os.urandom(16)
    
    ciphertext = b''
    feedback = bytes([iv[i] ^ key[i % len(key)] for i in range(16)])  # Initial encryption
    
    for i in range(0, len(plaintext), 16):
        block = plaintext.encode()[i:i+16]
        # XOR plaintext with feedback
        encrypted_block = bytes([block[j] ^ feedback[j] for j in range(len(block))])
        ciphertext += encrypted_block
        # Generate next feedback
        feedback = bytes([feedback[j] ^ key[j % len(key)] for j in range(len(feedback))])
    
    return base64.b64encode(iv + ciphertext).decode()

def simple_ofb_decrypt(ciphertext, key):
    data = base64.b64decode(ciphertext)
    iv = data[:16]
    ciphertext_blocks = data[16:]
    
    decrypted = b''
    feedback = bytes([iv[i] ^ key[i % len(key)] for i in range(16)])
    
    for i in range(0, len(ciphertext_blocks), 16):
        block = ciphertext_blocks[i:i+16]
        # XOR ciphertext with feedback
        decrypted_block = bytes([block[j] ^ feedback[j] for j in range(len(block))])
        decrypted += decrypted_block
        # Generate next feedback
        feedback = bytes([feedback[j] ^ key[j % len(key)] for j in range(len(feedback))])
    
    return decrypted.decode()

# Take user input
plaintext = input("Enter the plaintext message: ")
key_input = input("Enter the key (16 characters): ")

# Validate key length
if len(key_input) != 16:
    print("Error: Key must be exactly 16 characters long.")
    exit(1)

key = key_input.encode()

encrypted = simple_ofb_encrypt(plaintext, key)
decrypted = simple_ofb_decrypt(encrypted, key)

print(f"Simplified OFB Mode:")
print(f"Original: {plaintext}")
print(f"Encrypted: {encrypted}")
print(f"Decrypted: {decrypted}")
