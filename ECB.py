import base64

# Simplified ECB mode ---------------------------------------------------------------
def simple_ecb_encrypt(plaintext, key):
    # Pad the plaintext to be multiple of 16 bytes
    padding_length = 16 - (len(plaintext) % 16)
    padded_text = plaintext.encode() + bytes([padding_length] * padding_length)
    
    # Split into 16-byte blocks
    blocks = [padded_text[i:i+16] for i in range(0, len(padded_text), 16)]
    
    # Simple XOR "encryption" (in real AES this would be much more complex)
    ciphertext = b''
    for block in blocks:
        encrypted_block = bytes([block[i] ^ key[i % len(key)] for i in range(16)])
        ciphertext += encrypted_block
    
    return base64.b64encode(ciphertext).decode()

def simple_ecb_decrypt(ciphertext, key):
    # Decode from base64
    ciphertext = base64.b64decode(ciphertext)
    
    # Split into 16-byte blocks
    blocks = [ciphertext[i:i+16] for i in range(0, len(ciphertext), 16)]
    
    # Simple XOR "decryption"
    decrypted = b''
    for block in blocks:
        decrypted_block = bytes([block[i] ^ key[i % len(key)] for i in range(16)])
        decrypted += decrypted_block
    
    # Remove padding
    padding_length = decrypted[-1]
    return decrypted[:-padding_length].decode()

# Take key input from user and ensure it's 16 bytes
key_input = input("Enter key (16 characters): ")
while len(key_input) != 16:
    print("Error: Key must be exactly 16 characters.")
    key_input = input("Enter key (16 characters): ")

key = key_input.encode()

# Take plaintext input from user
plaintext = input("Enter plaintext to encrypt: ")

# Encrypt and decrypt
encrypted = simple_ecb_encrypt(plaintext, key)
decrypted = simple_ecb_decrypt(encrypted, key)

print(f"\nSimplified ECB Mode:")
print(f"Original: {plaintext}")
print(f"Encrypted: {encrypted}")
print(f"Decrypted: {decrypted}")
