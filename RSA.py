import random

# ==================  RSA ALGO ==================

def is_prime(number):
    if number < 2:
        return False
    for i in range(2, number // 2+1):
        if number % i == 0:
            return False
    return True

def generate_prime(min_value, max_value):
    prime = random.randint(min_value, max_value)
    while not is_prime(prime):
        prime = random.randint(min_value, max_value)
    return prime

def mod_inverse(e, phi):
    for d in range(3, phi):
        if (d * e) % phi == 1:
            return d
    return ValueError('No mod inverse found')

def encrypt_rsa(msg, e, n):
    msg_encoded = [ord(c) for c in msg]
    # (m^e) mod n = chipertext
    # pow(c, e, n) = c^e mod n
    chipertext = [pow(c, e, n) for c in msg_encoded]
    return chipertext

def decrypt_rsa(chipertext, d, n):
    # decryption
	msg_encoded = [pow(ch, d, n) for ch in chipertext]
	msg = ''.join([chr(c) for c in msg_encoded])
	return msg