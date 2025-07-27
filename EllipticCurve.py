def inverse_mod(k, p):
    """Compute the modular inverse of k modulo p."""
    return pow(k, -1, p)

def is_on_curve(x, y, a, b, p):
    """Check if the point lies on the curve."""
    return (y**2 - (x**3 + a*x + b)) % p == 0

def point_add(P, Q, a, p):
    """Add two points on the elliptic curve."""
    if P is None: return Q
    if Q is None: return P
    if P == Q:
        if P[1] == 0:
            return None
        m = (3 * P[0] ** 2 + a) * inverse_mod(2 * P[1], p)
    else:
        if P[0] == Q[0]:
            return None
        m = (Q[1] - P[1]) * inverse_mod(Q[0] - P[0], p)

    m %= p
    rx = (m * m - P[0] - Q[0]) % p
    ry = (m * (P[0] - rx) - P[1]) % p
    return (rx, ry)

def scalar_mult(k, P, a, p):
    """Multiply point P by scalar k on curve with 'a' coefficient and modulus 'p'."""
    result = None
    while k:
        if k & 1:
            result = point_add(result, P, a, p)
        P = point_add(P, P, a, p)
        k >>= 1
    return result

# Helper functions to convert between letters and numbers
def char_to_num(c):
    return ord(c) - ord('A')

def num_to_char(n):
    return chr(n + ord('A'))

# ----------- Input Section -----------
print("Elliptic Curve: y² = x³ + ax + b over field modulo p")

a = int(input("Enter coefficient a: "))
b = int(input("Enter coefficient b: "))
p = int(input("Enter prime modulus p: "))

gx = int(input("Enter base point G's x-coordinate: "))
gy = int(input("Enter base point G's y-coordinate: "))
G = (gx, gy)

if not is_on_curve(gx, gy, a, b, p):
    print("Error: G is not on the curve!")
    exit()

private_key_A = int(input("Enter sender's private key (A): "))
private_key_B = int(input("Enter receiver's private key (B): "))

# Generate public keys
public_key_A = scalar_mult(private_key_A, G, a, p)
public_key_B = scalar_mult(private_key_B, G, a, p)

print(f"Sender's Public Key: {public_key_A}")
print(f"Receiver's Public Key: {public_key_B}")

# Message to encrypt (letters only, uppercase)
msg = input("Enter message (letters only, uppercase): ").replace(" ", "")

# Encrypt each character
import random
k = random.randint(1, p-1)
C1 = scalar_mult(k, G, a, p)
S = scalar_mult(k, public_key_B, a, p)

ciphertext = []
for ch in msg:
    m_num = char_to_num(ch)
    c_num = (m_num * S[0]) % p
    ciphertext.append(c_num)

print("\n--- Encryption ---")
print(f"C1 (Ephemeral Public Key): {C1}")
print(f"Ciphertext numbers: {ciphertext}")

# Decrypt
S_prime = scalar_mult(private_key_B, C1, a, p)
S_inv = inverse_mod(S_prime[0], p)

decrypted_msg = ""
for c_num in ciphertext:
    m_num = (c_num * S_inv) % p
    decrypted_msg += num_to_char(m_num)

print("\n--- Decryption ---")
print(f"Shared Secret S': {S_prime}")
print(f"Decrypted Message: {decrypted_msg}")
