#Declearing the function For encryption.
def encrypt_caesar(plaintext,key):
    ciphertext=""
    for char in plaintext:
        if char.isalpha():
            shift=key%26
            if char.isupper():
               base=ord('A')
            else:
                base=ord('a')
            ciphertext+=chr((ord(char)-base+shift)%26+base)
        else:
            ciphertext +=char
    return ciphertext

#Declearing the function For dencryption.
def decrypt_caesar(ciphertext,key):
    return encrypt_caesar(ciphertext,-key)

#Take the input from the user
message=input("Enter your message: ")
key=int(input("Enter your shift key (0-25): "))

#Print the encrypted message
encrypted=encrypt_caesar(message,key)
print("Encrypted: ",encrypted)

#Print the decrypted message
decrypted=decrypt_caesar(encrypted,key)
print("Decrypted: ",decrypted)