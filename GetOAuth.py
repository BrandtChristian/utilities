import requests
from base64 import b64encode
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access the variables
api_key = os.getenv('TP_API_KEY')
api_secret = os.getenv('TP_API_SECRET')
username = os.getenv('TP_USERNAME')
password = os.getenv('TP_PASSWORD')

# Endpoint for obtaining an access token
token_url = 'https://api.trustpilot.com/v1/oauth/oauth-business-users-for-applications/accesstoken'

# Encode the API key and secret
credentials = f"{api_key}:{api_secret}"
encoded_credentials = b64encode(credentials.encode('utf-8')).decode('utf-8')

# Headers
headers = {
    'Authorization': f'Basic {encoded_credentials}',
    'Content-Type': 'application/x-www-form-urlencoded'
}

# Payload
payload = {
    'grant_type': 'password',
    'username': username,
    'password': password
}

# Make the request
response = requests.post(token_url, headers=headers, data=payload)

# Check for successful response
if response.status_code == 200:
    # Extract the access token from the response
    access_token = response.json().get('access_token')
    refresh_token = response.json().get('refresh_token')
    expires_in = response.json().get('expires_in')
    
    print("Access Token:", access_token)
    print("Refresh Token:", refresh_token)
    print("Expires In:", expires_in)
else:
    print("Failed to obtain access token. Status code:", response.status_code)
    print("Response:", response.text)
