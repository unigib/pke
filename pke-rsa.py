import random

# 1. Key Generation
def generate_keys(p, q):
    """Generates RSA keys (public, private) based on two primes."""
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # Choose encryption exponent e
    e = 65537 # Common choice
    
    # Calculate decryption exponent d (modular inverse)
    d = pow(e, -1, phi) 
    
    # Public Key (e, n), Private Key (d, n)
    return ((e, n), (d, n))

# 2. Encryption
def encrypt(message, public_key):
    """Encrypts a numeric message: c = m^e mod n"""
    e, n = public_key
    #pow(base, exp, mod) is efficient modular exponentiation
    cipher = [pow(ord(char), e, n) for char in message]
    return cipher

# 3. Decryption
def decrypt(cipher, private_key):
    """Decrypts a cipher list: m = c^d mod n"""
    d, n = private_key
    message = [chr(pow(char, d, n)) for char in cipher]
    return ''.join(message)

# --- Usage Example ---
# Use small primes for demonstration (not secure in practice)
p = 61
q = 53
pub, priv = generate_keys(p, q)

print(f"Public Key: {pub}")
print(f"Private Key: {priv}")

message = "Gib University is great"
encrypted_msg = encrypt(message, pub)
decrypted_msg = decrypt(encrypted_msg, priv)

print(f"Original: {message}")
print(f"Encrypted (numeric): {encrypted_msg}")
print(f"Decrypted: {decrypted_msg}")
