from cryptography.fernet import Fernet

def generate_key():
    """Generates a key and saves it to a file"""
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    print("Key generated and saved as secret.key")

def load_key():
    """Loads the key from the current directory"""
    return open("secret.key", "rb").read()

def encrypt_message(message):
    """Encrypts a message"""
    key = load_key()
    f = Fernet(key)
    # Convert message to bytes before encryption
    encrypted_message = f.encrypt(message.encode())
    return encrypted_message

def decrypt_message(encrypted_message):
    """Decrypts a message"""
    key = load_key()
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message)
    # Convert bytes back to string
    return decrypted_message.decode()

# --- Execution ---
# 1. Generate and save a key (only run once)
generate_key()

# 2. Encrypt
message = "Top Secret Message for Undergrads"
encrypted = encrypt_message(message)
print(f"Encrypted: {encrypted}")

# 3. Decrypt
decrypted = decrypt_message(encrypted)
print(f"Decrypted: {decrypted}")
