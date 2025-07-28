#Define the function for Key square generation.
def make_key_square(key):

    key = key.replace("J", "I").upper()
    chars = []
    
    # Add unique letters from key
    for char in key:
        if char.isalpha() and char not in chars:
            chars.append(char)
    
    # Add rest of alphabet (no J)
    for char in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if char not in chars:
            chars.append(char)
    
    # Create 5x5 grid using simple loop
    grid = []
    for i in range(0, 25, 5):
        row = chars[i:i+5]
        grid.append(row)
    
    return grid

#Prepare Text Espically handel the double and odd values
def prepare_text(text):
    text = text.replace("J", "I")  # Replace J with I
    text = text.upper()           # Convert to uppercase
    text = text.replace(" ", "")  # Remove spaces
    result = ""
    i = 0
    while i < len(text):
        a = text[i]  # First character
        # Check if there is a next character
        if i + 1 < len(text):
            b = text[i + 1]  # Second character
        else:
            b = "X"  # If no next character, use 'X'
        # If both letters are same (like LL), insert 'X' between them
        if a == b:
            result += a + "X"
            i += 1
        else:
            result += a + b
            i += 2
    # If the result length is odd, add 'X' at the end
    if len(result) % 2 != 0:
        result += "X"
    return result

#This function find the position of the text
def find_position(square, char):
    for r in range(5):
        for c in range(5):
            if square[r][c] == char:
                return r, c
            
#This function define the rule of encryption for two latter
def encrypt_pair(a, b, square):
    r1, c1 = find_position(square, a)
    r2, c2 = find_position(square, b)

    if r1 == r2:  # Same row
        return square[r1][(c1 + 1) % 5] + square[r2][(c2 + 1) % 5]
    elif c1 == c2:  # Same column
        return square[(r1 + 1) % 5][c1] + square[(r2 + 1) % 5][c2]
    else:  # Rectangle
        return square[r1][c2] + square[r2][c1]
    
#Define the function for encryption 
def playfair_encrypt(text, key):
    square = make_key_square(key)
    prepared = prepare_text(text)
    cipher = ""
    for i in range(0, len(prepared), 2):
        a, b = prepared[i], prepared[i+1]
        cipher += encrypt_pair(a, b, square)
    return cipher

# Define the rule of decryption for a pair of letters
def decrypt_pair(a, b, square):
    r1, c1 = find_position(square, a)
    r2, c2 = find_position(square, b)

    if r1 == r2:  # Same row: move left
        return square[r1][(c1 - 1) % 5] + square[r2][(c2 - 1) % 5]
    elif c1 == c2:  # Same column: move up
        return square[(r1 - 1) % 5][c1] + square[(r2 - 1) % 5][c2]
    else:  # Rectangle swap columns
        return square[r1][c2] + square[r2][c1]

# Define the function for decryption
def playfair_decrypt(cipher, key):
    square = make_key_square(key)
    cipher = cipher.upper().replace(" ", "")  # Clean input
    plaintext = ""
    for i in range(0, len(cipher), 2):
        a, b = cipher[i], cipher[i+1]
        plaintext += decrypt_pair(a, b, square)
    return plaintext

# Get user input
key = input("Enter the key (letters only): ")
text = input("Enter the plaintext to encrypt: ")

print(f"\nText: {text}")
print(f"Key: {key}")

encrypted = playfair_encrypt(text, key)
print(f"Encrypted: {encrypted}")

decrypted = playfair_decrypt(encrypted, key)
print(f"Decrypted: {decrypted}")