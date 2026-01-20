import os
import json
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

class FinancialSecurity:
    """
    AES-256-GCM Security Layer for DANIEL_AI Financial Division.
    Provides encryption, decryption, and secure hashing for sensitive financial data.
    """
    def __init__(self, master_key: str = None):
        if not master_key:
            master_key = os.getenv("FINANCIAL_MASTER_KEY", "default-dev-key-do-not-use-in-prod")
        
        # Derive a 256-bit key from the master_key
        salt = b"daniel-ai-financial-salt"
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        self.key = kdf.derive(master_key.encode())
        self.aesgcm = AESGCM(self.key)

    def encrypt(self, data: str) -> str:
        """Encrypts data using AES-256-GCM and returns a base64 encoded string."""
        nonce = os.urandom(12)
        encoded_data = data.encode()
        ciphertext = self.aesgcm.encrypt(nonce, encoded_data, None)
        # Combined: [nonce(12)][ciphertext]
        result = nonce + ciphertext
        return base64.b64encode(result).decode('utf-8')

    def decrypt(self, encrypted_data: str) -> str:
        """Decrypts a base64 encoded AES-256-GCM string."""
        raw_data = base64.b64decode(encrypted_data)
        nonce = raw_data[:12]
        ciphertext = raw_data[12:]
        decrypted_data = self.aesgcm.decrypt(nonce, ciphertext, None)
        return decrypted_data.decode('utf-8')

    def hash_id(self, identifier: str) -> str:
        """Securely hashes an identifier (e.g. SSN or Wallet) for ZKP related lookups."""
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(identifier.encode())
        return digest.finalize().hex()
