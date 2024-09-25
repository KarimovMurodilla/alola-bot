import hmac
import hashlib
import base64
import json
import time

# Function to encode in Base64URL without padding
def base64url_encode(data):
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('utf-8')

# Secret key
secret = ""

# JWT Header and Payload
header = {
    "typ": "JWT",
    "alg": "HS256"
}
payload = {
    "iss": "alola.uzvip.uz",
    "iat": int(time.time()),
    "exp": 1738553677,
    "sub": "shop_bot"
}

# Encode header and payload in Base64URL
encoded_header = base64url_encode(json.dumps(header).encode())
encoded_payload = base64url_encode(json.dumps(payload).encode())

# Create the unsigned token (header + '.' + payload)
unsigned_token = f"{encoded_header}.{encoded_payload}"

# Create the signature using HMAC-SHA256
signature = hmac.new(secret.encode(), unsigned_token.encode(), hashlib.sha256).digest()

# Base64URL encode the signature
encoded_signature = base64url_encode(signature)

# Form the final JWT token
token = f"{unsigned_token}.{encoded_signature}"

# Output the token
print(token)
