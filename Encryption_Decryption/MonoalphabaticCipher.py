#Import all necessary library
import random
import string

#Create the alphabate and a suffled version for the key
alphabet=list(string.ascii.uppercase)
cipher_alphabet=alphabet.copy()
random.shuffle(cipher_alphabet)

#create encryption and decryption maps
encrypt_map=dict(zip(alphabet,cipher_alphabet))
decrypt_map=dict(zip(cipher_alphabet,alphabet))

#Take the Input message
msg=input("Enter the message to encrypt (A-Z only): ").upper()

#Encrypt the message
encrypted=""
for ch in msg:
    if ch in encrypt_map:
        encrypted+=encrypt_map[ch]
    else:
        encrypted+=ch

#Decrypt the message
decrypted=""
for ch in encrypted:
    if ch in decrypted:
        decrypted+=decrypt_map[ch]
    else:
        decrypted+=ch