import hashlib

def one_way_encrypt(data: str) -> str:
    """
    Takes a string input and returns its SHA-256 hash.
    """
    # 1. Encode the string to bytes
    encoded_data = data.encode('utf-8')
    
    # 2. Create a SHA-256 hash object
    sha256_hash = hashlib.sha256()
    
    # 3. Update the hash object with the bytes
    sha256_hash.update(encoded_data)
    
    # 4. Return the hexadecimal representation of the hash
    return sha256_hash.hexdigest()

# Example Usage
password = "my_secure_password"
encrypted_password = one_way_encrypt(password)

print(f"Original: {password}")
print(f"Encrypted: {encrypted_password}")
# Output will be a fixed-length string, regardless of input size.
