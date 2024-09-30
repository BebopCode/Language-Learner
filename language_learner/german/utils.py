import google.auth.transport.requests
from google.oauth2 import id_token
from django.conf import settings
from dotenv import load_dotenv
import os
load_dotenv()
client_id=os.getenv('CLIENT_ID')

def validate_google_token(token):
    try:
        # Initialize the verifier with your app's client ID
        request = google.auth.transport.requests.Request()
        idinfo = id_token.verify_oauth2_token(token, request, client_id)
        
        # The ID token contains user information
        return idinfo
    except ValueError as e:
        # Invalid token
        print(f"Token validation error: {e}")
        return None
