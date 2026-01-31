import hashlib
import json
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class SafeEncryption:
    def __init__(self, client_secret=None):
        secret = client_secret or os.getenv('SAFECORE_CLIENT_SECRET')
        if not secret:
            secret = "DANIEL_AI_TEMPORARY_SECRET_DEV_ONLY"
        self.key = hashlib.sha256(secret.encode()).digest()

    def encrypt(self, payload: dict) -> dict:
        aesgcm = AESGCM(self.key)
        iv = os.urandom(16)
        data_json = json.dumps(payload, separators=(',', ':')).encode()
        ciphertext_with_tag = aesgcm.encrypt(iv, data_json, None)
        data = ciphertext_with_tag[:-16].hex()
        tag = ciphertext_with_tag[-16:].hex()
        return {"iv": iv.hex(), "data": data, "tag": tag}

    def decrypt(self, encrypted_payload: dict) -> dict:
        try:
            iv = bytes.fromhex(encrypted_payload['iv'])
            data = bytes.fromhex(encrypted_payload['data'])
            tag = bytes.fromhex(encrypted_payload['tag'])
            aesgcm = AESGCM(self.key)
            decrypted_data = aesgcm.decrypt(iv, data + tag, None)
            return json.loads(decrypted_data.decode())
        except Exception as e:
            raise ValueError(f"Decryption failed: {str(e)}")
