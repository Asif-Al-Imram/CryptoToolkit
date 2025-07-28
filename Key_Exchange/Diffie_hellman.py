#Function for performing the modular exponentiation.
def power(base,exponent,modulus):
    return pow(base,exponent,modulus)

#Step-1 Both the parties agree on public values.
#A larger prime number (p) and a primitive root modulo p (g)
#Take input from the user
p=int(input("Enter a prime number (p): "))
g=int(input("Enter a primitive root modulo p(g): "))

#Each party agree on a parivte key
a=int(input("Enter Alice's private key (a): "))
b=int((input("Enter Bob's private key (b): ")))

#Each generatr their own public key
Pub_of_alice=power(g,a,p)
pub_of_bob=power(g,b,p)

#Show their Public key
print(f"Public key of Alice: {Pub_of_alice}")
print(f"Public key of Bob {pub_of_bob}")

#Each party computes the shared secret key
shared_key_Alice=power(pub_of_bob,a,p)
shared_key_Bob=power(Pub_of_alice,b,p)

#Show their Shared key
print(f"Alices's shared key: {shared_key_Alice}")
print(f"Bob's shared key: {shared_key_Bob}")

if shared_key_Alice==shared_key_Bob:
    print(f"Key exchange successfull!")
else:
    print(f"Key exchange failed!")
