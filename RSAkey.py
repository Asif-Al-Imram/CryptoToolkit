import random

#GCD Algorithm
def gcd(a,b):
    while b!=0:
        a,b=b,a%b
    return a

#Extended Euclidean
def extended_euclidean(a,b):
    if a==0:
      return b,0,1
    gcd_,x1,y1 = extended_euclidean(b%a,a)
    x= y1 - (b // a) * x1
    y=x1
    return gcd_,x,y

def mod_inverse(e,phi):
    gcd_,x,_=extended_euclidean(e,phi)
    if gcd_ !=1:
        raise Exception("Modular inversr does not exist")
    else:
        return x % phi

#Check the number whether it is prime or not.
def is_prime(n):
    if n<=1:
        return False
    for i in range(2,int(n**0.5)+1):
        if n%i==0:
            return False
    return True

#Public key generation
def generate_public_key(phi, n):
    while True:
        e=random.randint(2, phi-1)
        if gcd(e,phi):
            break
        return(e,n)
    
#private key Generation
def generate_private_key(e,phi,n):
    d=mod_inverse(e,phi)
    return(d,n)

#RSA key generation
def generate_keys():
    p=int(input("Enter a prime number p: "))
    q=int(input("Enter a primr number q: "))
    n=p*q
    phi=(p-1)*(q-1)
    public_key=generate_public_key(phi,n)
    private_key=generate_private_key(public_key[0],phi,n)

    print(f"\nPublic Key (e,n): {public_key}")
    print(f"Private Key (d,n): {private_key}")
    return public_key,private_key