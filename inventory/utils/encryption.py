from cryptography.fernet import Fernet
from django.conf import settings
import json

encryption_key = Fernet(settings.ENCRYPTION_KEY)

def encrypt_credentials(data: dict) -> str:
    try:
        json_data = json.dumps(data).encode()
        encrypted = encryption_key.encrypt(json_data)
        return encrypted.decode()
    except:
        return None

def decrypt_credentials(token: str) -> dict:

    try:
        decrypted = encryption_key.decrypt(token.encode())
        return json.loads(decrypted.decode())
    except:
        return None