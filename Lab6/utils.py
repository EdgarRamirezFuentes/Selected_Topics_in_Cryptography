from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes


def generate_keys(username):
    """Generate private and public keys and save them to files.
    
    Args:
        username (str): The username of the user.
        
    Returns:
        bool: True if the keys were generated successfully, False otherwise.
    """
    try:
        # Key generation
        private_key = ec.generate_private_key(ec.SECP384R1())

        with open(f"./private_signatures/{username}_private_key.pem", "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))

        public_key = private_key.public_key()

        with open(f"./public_signatures/{username}_public_key.pem", "wb") as f:
            f.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))

        return True
    except Exception as e:
        print(e)
        return False
    

def load_keys(username):
    """Load private and public keys from files.
    
    Args:
        username (str): The username of the user.
        
    Returns:
        tuple: The private and public keys.
    """
    try:
        with open(f"./private_signatures/{username}_private_key.pem", "rb") as f:
            private_key = serialization.load_pem_private_key(
                f.read(),
                password=None,
                backend=default_backend()
            )

        with open(f"./public_signatures/{username}_public_key.pem", "rb") as f:
            public_key = serialization.load_pem_public_key(
                f.read(),
                backend=default_backend()
            )

        return private_key, public_key
    except Exception as e:
        print(e)
        return None, None
    

def sign_file(username, data):
    """Sign a file with the user's private key.
    
    Args:
        username (str): The username of the user.
        data (bytes): The data to sign.
        
    Returns:
        bytes: The signature.
    """
    try:
        private_key, _ = load_keys(username)
        
        signature = private_key.sign(
            data,
            ec.ECDSA(hashes.SHA256())
        )
        
        return signature
    except Exception as e:
        print(e)
        return None
    

def verify_signature(username, data, signature):
    """Verify the signature of a file.
    
    Args:
        username (str): The username of the user.
        data (bytes): The data to verify.
        signature (bytes): The signature to verify.
        
    Returns:
        bool: True if the signature is valid, False otherwise.
    """
    try:
        _, public_key = load_keys(username)
        
        public_key.verify(
            signature,
            data,
            ec.ECDSA(hashes.SHA256())
        )
        
        return True
    except Exception as e:
        print(e)
        return False