class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"({self.x}, {self.y})"

class TinyECC:
    def __init__(self):
        # Using a tiny curve: y² = x³ + 2x + 2 mod 17
        self.a = 2
        self.b = 2
        self.p = 17
    
    def add(self, P, Q):
        if P.x == 0 and P.y == 0: return Q
        if Q.x == 0 and Q.y == 0: return P
        if P.x == Q.x and P.y != Q.y: return Point(0, 0)
        
        if P != Q:
            # Slope for point addition
            m = (Q.y - P.y) * pow(Q.x - P.x, -1, self.p) % self.p
        else:
            # Slope for point doubling
            m = (3 * P.x**2 + self.a) * pow(2 * P.y, -1, self.p) % self.p
        
        x_r = (m**2 - P.x - Q.x) % self.p
        y_r = (m * (P.x - x_r) - P.y) % self.p
        
        return Point(x_r, y_r)
    
    def multiply(self, P, n):
        result = Point(0, 0)
        current = P
        
        while n > 0:
            if n % 2 == 1:
                result = self.add(result, current)
            current = self.add(current, current)
            n = n // 2
        
        return result

# Create our tiny curve
tiny_curve = TinyECC()

# Take inputs from the user
p = int(input("Enter prime modulus p (e.g. 17): "))
a = int(input("Enter curve coefficient a (e.g. 2): "))
b = int(input("Enter curve coefficient b (e.g. 2): "))

tiny_curve.p = p
tiny_curve.a = a
tiny_curve.b = b

gx = int(input("Enter base point G's x-coordinate (e.g. 5): "))
gy = int(input("Enter base point G's y-coordinate (e.g. 1): "))
G = Point(gx, gy)

alice_private = int(input("Enter Alice's private key (e.g. 3): "))
bob_private = int(input("Enter Bob's private key (e.g. 7): "))

alice_public = tiny_curve.multiply(G, alice_private)
bob_public = tiny_curve.multiply(G, bob_private)

print("\nTiny ECC Example")
print("---------------")
print(f"Base point G: {G}")
print(f"Alice's private key: {alice_private}")
print(f"Alice's public key: {alice_public}")
print(f"Bob's private key: {bob_private}")
print(f"Bob's public key: {bob_public}")

alice_shared = tiny_curve.multiply(bob_public, alice_private)
bob_shared = tiny_curve.multiply(alice_public, bob_private)

print("\nKey Exchange Results:")
print(f"Alice's shared secret: {alice_shared}")
print(f"Bob's shared secret: {bob_shared}")
print(f"Secrets match: {alice_shared == bob_shared}")

def super_simple_encrypt(public_key, message, secret, p):
    shared_point = public_key
    for _ in range(secret-1):
        shared_point = (
            (shared_point[0] + public_key[0]) % p,
            (shared_point[1] + public_key[1]) % p
        )
    key = shared_point[0] % 256
    encrypted = ''.join([chr(ord(c) ^ key) for c in message])
    return encrypted

def super_simple_decrypt(encrypted, public_key, secret, p):
    shared_point = public_key
    for _ in range(secret-1):
        shared_point = (
            (shared_point[0] + public_key[0]) % p,
            (shared_point[1] + public_key[1]) % p
        )
    key = shared_point[0] % 256
    decrypted = ''.join([chr(ord(c) ^ key) for c in encrypted])
    return decrypted

message = input("\nEnter the message to encrypt: ")
secret = int(input("Enter secret multiplier (integer): "))
pub_x = int(input("Enter public key x-coordinate: "))
pub_y = int(input("Enter public key y-coordinate: "))
public_key = (pub_x, pub_y)

encrypted = super_simple_encrypt(public_key, message, secret, p)
decrypted = super_simple_decrypt(encrypted, public_key, secret, p)

print("\nOriginal:", message)
print("Encrypted:", encrypted)
print("Decrypted:", decrypted)
