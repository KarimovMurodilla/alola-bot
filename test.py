import base64
import hmac
import hashlib

# Function to encode in Base64URL without padding
def base64url_encode(data):
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('utf-8')

# Function to generate the HMAC SHA-256 signature
def create_signature(unsigned_token, secret_key):
    return hmac.new(secret_key.encode(), unsigned_token.encode(), hashlib.sha256).digest()

# Example JWT header and payload
header = '{"alg":"HS256","typ":"JWT"}'
payload = '{"iss": "example.com","iat": 1522402972,"exp": 1522403092,"sub": "shop_bot"}'

# Secret key
secret_key = 'f892bd264f9b0e19c87ed570a7d5b3712ef5329f491cea682d962f79dedc96da883d4abbb6243809d45b1afb761831071dcf51208927d91a9330f500b29062a077ff9c3736ec8bf8b993e97c844c459d67d8678f165a80e60b9575ef4fd0de606c44acb2a2f792a0167434a01d4b889580f23721f49bc00f'

# Base64URL encode header and payload
encoded_header = base64url_encode(header.encode())
encoded_payload = base64url_encode(payload.encode())

# Create the unsigned token (header + '.' + payload)
unsigned_token = f"{encoded_header}.{encoded_payload}"

# Create the signature using HMAC-SHA256
signature = create_signature(unsigned_token, secret_key)

# Base64URL encode the signature
encoded_signature = base64url_encode(signature)

# Form the final JWT token
token = f"{encoded_header}.{encoded_payload}.{encoded_signature}"

print("JWT Token:", token)
