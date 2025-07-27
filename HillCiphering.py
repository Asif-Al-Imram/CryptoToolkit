#Function to convert letter into number
def letter_to_num(c):
    return ord(c.upper()) - ord('A')

#Function to convert number into letter
def num_to_letter(n, original_char):
    letter = chr(n % 26 + ord('A'))
    return letter.lower() if original_char.islower() else letter

#Function to find mod inverse
def mod_inverse(a, m=26):
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    return None

#Function to definr inverse function
def inverse_matrix_2x2(matrix):
    a, b = matrix[0]
    c, d = matrix[1]
    det = (a * d - b * c) % 26
    det_inv = mod_inverse(det)
    if det_inv is None:
        raise ValueError("Matrix is not invertible")

    return [
        [( d * det_inv) % 26, (-b * det_inv) % 26],
        [(-c * det_inv) % 26, ( a * det_inv) % 26]
    ]

#Function for adding the extra letter
def pad_text(text):
    letters = [ch for ch in text if ch.isalpha()]
    if len(letters) % 2 != 0:
        text += 'X'  # Append 'X' if number of letters is odd
    return text

#Function for Encryption
def hill_encrypt(plaintext, key):
    result = ""
    buffer = []

    for ch in plaintext:
        if ch.isalpha():
            buffer.append(ch)
            if len(buffer) == 2:
                p1 = letter_to_num(buffer[0])
                p2 = letter_to_num(buffer[1])
                c1 = (key[0][0] * p1 + key[0][1] * p2) % 26
                c2 = (key[1][0] * p1 + key[1][1] * p2) % 26
                result += num_to_letter(c1, buffer[0])
                result += num_to_letter(c2, buffer[1])
                buffer = []
        else:
            result += ch

    # In case one letter left unprocessed (odd number of letters)
    if len(buffer) == 1:
        p1 = letter_to_num(buffer[0])
        p2 = letter_to_num('X')
        c1 = (key[0][0] * p1 + key[0][1] * p2) % 26
        c2 = (key[1][0] * p1 + key[1][1] * p2) % 26
        result += num_to_letter(c1, buffer[0])
        result += num_to_letter(c2, 'X')

    return result

#Function to define decryption
def hill_decrypt(ciphertext, key):
    inverse_key = inverse_matrix_2x2(key)
    result = ""
    buffer = []

    for ch in ciphertext:
        if ch.isalpha():
            buffer.append(ch)
            if len(buffer) == 2:
                c1 = letter_to_num(buffer[0])
                c2 = letter_to_num(buffer[1])
                p1 = (inverse_key[0][0] * c1 + inverse_key[0][1] * c2) % 26
                p2 = (inverse_key[1][0] * c1 + inverse_key[1][1] * c2) % 26
                result += num_to_letter(p1, buffer[0])
                result += num_to_letter(p2, buffer[1])
                buffer = []
        else:
            result += ch

    return result

# --- User Input ---
print("Enter the 2x2 key matrix values row-wise, numbers between 0-25.")
row1 = list(map(int, input("Enter first row (2 numbers separated by space): ").split()))
row2 = list(map(int, input("Enter second row (2 numbers separated by space): ").split()))
if len(row1) != 2 or len(row2) != 2:
    print("Error: Please enter exactly 2 numbers per row.")
    exit(1)
key_matrix = [row1, row2]

try:
    inverse_matrix_2x2(key_matrix)  # Check invertibility
except ValueError as e:
    print("Error:", e)
    exit(1)

plaintext = input("Enter plaintext: ")
ciphertext = hill_encrypt(plaintext, key_matrix)
print("Encrypted text:", ciphertext)
decrypted = hill_decrypt(ciphertext, key_matrix)
print("Decrypted text:", decrypted)