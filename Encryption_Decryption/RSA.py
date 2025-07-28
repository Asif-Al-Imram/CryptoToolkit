import random

# GCD Algorithm
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# Extended Euclidean Algorithm to find modular inverse
def extended_euclidean(a, b):
    if a == 0:
        return b, 0, 1
    gcd_, x1, y1 = extended_euclidean(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd_, x, y

# Modular inverse using extended Euclidean algorithm
def mod_inverse(e, phi):
    gcd_, x, _ = extended_euclidean(e, phi)
    if gcd_ != 1:
        raise Exception("Modular inverse does not exist")
    else:
        return x % phi

# Check if a number is prime
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# Generate public key (e, n)
def generate_public_key(phi, n):
    while True:
        e = random.randint(2, phi - 1)
        if gcd(e, phi) == 1:  # e must be coprime with phi
            break
    return (e, n)

# Generate private key (d, n)
def generate_private_key(e, phi, n):
    d = mod_inverse(e, phi)
    return (d, n)

# RSA key generation
def generate_keys():
    p = int(input("Enter a prime number p: "))
    q = int(input("Enter a prime number q: "))

    # Validate primes
    if not is_prime(p) or not is_prime(q):
        print("Both numbers must be prime.")
        return None, None

    n = p * q                      # RSA modulus
    phi = (p - 1) * (q - 1)        # Euler's totient function
    public_key = generate_public_key(phi, n)
    private_key = generate_private_key(public_key[0], phi, n)

    print(f"\nPublic Key (e, n): {public_key}")
    print(f"Private Key (d, n): {private_key}")
    return public_key, private_key

# Encrypt a message (as integer)
def encrypt(message, public_key):
    e, n = public_key
    cipher = pow(message, e, n)  # c = m^e mod n
    return cipher

# Decrypt a cipher (as integer)
def decrypt(cipher, private_key):
    d, n = private_key
    message = pow(cipher, d, n)  # m = c^d mod n
    return message

# ---------------------------
# Main Program
# ---------------------------
public_key, private_key = generate_keys()

if public_key and private_key:
    msg = int(input("\nEnter a message to encrypt (as number): "))
    
    cipher = encrypt(msg, public_key)       # Encrypt the message
    print("Encrypted message:", cipher)

    decrypted = decrypt(cipher, private_key)  # Decrypt the message
    print("Decrypted message:", decrypted)
