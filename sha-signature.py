# Undergraduate PKI Project: RSA & SHA-256 Signing
# Requirements: pip install cryptography

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

# 1. Key Generation (Done by Alice/Entity)
def generate_keys():
    # Generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    # Extract public key
    public_key = private_key.public_key()
    return private_key, public_key

# 2. Signing a Message (Alice signs)
def sign_message(private_key, message):
    message_bytes = message.encode('utf-8')
    signature = private_key.sign(
        message_bytes,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

# 3. Verifying the Signature (Bob/Other party verifies)
def verify_signature(public_key, message, signature):
    message_bytes = message.encode('utf-8')
    try:
        public_key.verify(
            signature,
            message_bytes,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except Exception as e:
        print(f"Verification failed: {e}")
        return False

# Example Usage
if __name__ == "__main__":
    # Setup
    print("Generating keys...")
    alice_private, alice_public = generate_keys()
    message = "Classified: Undergraduate Exam Paper!"
    
    # Signing
    signature = sign_message(alice_private, message)
    print(f"\nMessage: {message}")
    print(f"Signature (hex): {signature.hex()[:50]}...")

    # Verification
    is_valid = verify_signature(alice_public, message, signature)
    print(f"\nSignature Valid? {is_valid}")
    
    # Tamper Attempt
    tampered_message = "Classified: Undergraduate Exam Paper? No."
    is_valid_tampered = verify_signature(alice_public, tampered_message, signature)
    print(f"Tampered Signature Valid? {is_valid_tampered}")
