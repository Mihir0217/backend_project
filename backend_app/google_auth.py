from google_auth_oauthlib.flow import Flow
from django.http import JsonResponse
import os

CLIENT_SECRET_FILE = 'client_secret.json'
SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/drive.file"
]
REDIRECT_URI = 'http://localhost:8000/api/auth/callback/'

def google_login(request):
    flow = Flow.from_client_secrets_file(CLIENT_SECRET_FILE, scopes=SCOPES)
    flow.redirect_uri = REDIRECT_URI
    auth_url, _ = flow.authorization_url(prompt='consent')
    return JsonResponse({'auth_url': auth_url})

def google_callback(request):
    return JsonResponse({'message': 'User authenticated successfully'})
