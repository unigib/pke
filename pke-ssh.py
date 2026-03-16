# First, install the library: pip install cryptography
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def generate_ssh_key(filepath="id_rsa"):
    # 1. Generate the private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    # 2. Serialize and save the private key (PEM format)
    with open(filepath, "wb") as f:
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption(), # No password
            )
        )
    print(f"Private key saved to {filepath}")

    # 3. Generate and save the public key (OpenSSH format)
    public_key = private_key.public_key()
    with open(f"{filepath}.pub", "wb") as f:
        f.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.OpenSSH,
                format=serialization.PublicFormat.OpenSSH,
            )
        )
    print(f"Public key saved to {filepath}.pub")

# Generate the key pair
generate_ssh_key()
