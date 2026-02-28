from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

#RSA; asymmetrical encryption

#only used by server to generate a RSA pair at start
def generate_rsa_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,				#universal standard, very safe
        key_size=2048					#enough for high security and good speed
    )
    public_key = private_key.public_key()
    return private_key, public_key


#used to transform the public key from a python object into bytes; for transmitting the public key through the network
def serialize_public_key(public_key):
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,				#PEM = universal format
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )


#client receives the public key in bytes; uses this to transform it back into RSA object
def load_public_key(data):
    return serialization.load_pem_public_key(data)


#encrypts the AES key using the public RSA key of the server
def rsa_encrypt(public_key, plaintext_bytes):
    return public_key.encrypt(
        plaintext_bytes,
        padding.OAEP(						#OAEP padding used to avoid old RSA vulnerabilities;
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),				#OAEP + SHA256 = modern standard that's really safe
            label=None
        )
    )


#servers receives AES encrypted key and it decrypts it with the private_key
def rsa_decrypt(private_key, ciphertext):
    return private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )



#AES; symmetrical encryption


def generate_aes_key():
    return os.urandom(32)   # 256-bit key; AES-256 is the safest possible standard

#encrypts a message using AES
def aes_encrypt(key, plaintext):
    iv = os.urandom(16)						#iv (initialization vector) is used for avoiding repeating patterns; unique for each message
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv))		#we build an AES cipher in CFB (Cipher Feedback Mode) mode
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
    return iv + ciphertext					#for decrypting, the receiver needs to also know the iv


#decrypts a message using AES
def aes_decrypt(key, data):
    iv = data[:16]						#gets the iv of the message; always the first 16 bytes
    ciphertext = data[16:]					#gets the encrypted text
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext.decode()
