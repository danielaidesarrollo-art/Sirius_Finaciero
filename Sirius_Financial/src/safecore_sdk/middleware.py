from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from .encryption import SafeEncryption
import json
import os

class PhoenixDecryptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.headers.get('x-safecore-encrypted') != 'true':
            if os.getenv('ENFORCE_ENCRYPTION') == 'true' and request.method != 'GET':
                return Response(content=json.dumps({"error": "Encryption Required"}), status_code=403, media_type="application/json")
            return await call_next(request)
        try:
            body = await request.json()
            encryptor = SafeEncryption()
            decrypted_body = encryptor.decrypt(body)
            request.state.decrypted_body = decrypted_body
            request.state.is_encrypted = True
            return await call_next(request)
        except Exception as e:
            print(f"[SafeCore] Decryption Failed: {str(e)}")
            return Response(content=json.dumps({"error": "Decryption Failed"}), status_code=403, media_type="application/json")
