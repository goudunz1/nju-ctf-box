import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

fp=open("/flag","r")
flag=fp.read()
key=os.urandom(16)

def encrypt(plaintext):
    padded=pad(plaintext+flag.encode(),block_size=16)
    cipher=AES.new(key,AES.MODE_ECB)
    ciphertext=cipher.encrypt(padded)
    return ciphertext

def main():
    while True:
        try:
            plaintext=bytes.fromhex(input())
            ciphertext=encrypt(plaintext)
            print(ciphertext.hex())
        except:
            break

if __name__ == "__main__":
    main()

