# Import library
import base64

# Define the function for XOR operation
def xor_block(block, key):
    result = bytearray(len(block))
    for i in range(len(block)):
        result[i] = block[i] ^ key[i % len(key)]
    return bytes(result)

# Define the function for padding the input text
def pad(text, block_size):
    pad_len = block_size - (len(text) % block_size)
    return text + bytes([pad_len] * pad_len)

# Define the function for unpadding the text
def unpad(text):
    return text[:-text[-1]]

# Define the function for splitting into blocks (traditional loop)
def split_into_blocks(data, block_size):
    blocks = []
    i = 0
    while i < len(data):
        block = data[i:i + block_size]
        blocks.append(block)
        i += block_size
    return blocks

# Define the ECB encryption code
def simple_ecb_encrypt(plaintext, key, block_size):
    text_bytes = plaintext.encode()
    padded = pad(text_bytes, block_size)
    blocks = split_into_blocks(padded, block_size)

    ciphertext = b''
    for block in blocks:
        ciphertext += xor_block(block, key)
    return base64.b64encode(ciphertext).decode()

# Define the ECB decryption code
def simple_ecb_decrypt(ciphertext, key, block_size):
    data = base64.b64decode(ciphertext)
    blocks = split_into_blocks(data, block_size)

    decrypted = b''
    for block in blocks:
        decrypted += xor_block(block, key)
    return unpad(decrypted).decode()

# User input
key_input = input("Enter encryption key (any length): ")
key = key_input.encode()

while True:
    try:
        block_size = int(input("Enter block size (e.g., 8, 16, 32): "))
        if block_size <= 0:
            raise ValueError
        break
    except ValueError:
        print("Invalid input. Enter a positive number.")

plaintext = input("Enter plaintext to encrypt: ")

# Encryption & Decryption
encrypted = simple_ecb_encrypt(plaintext, key, block_size)
decrypted = simple_ecb_decrypt(encrypted, key, block_size)

# Output
print("Encrypted (Base64):", encrypted)
print("Decrypted:", decrypted)