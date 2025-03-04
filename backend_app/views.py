import json
from django.http import JsonResponse
from google_auth_oauthlib.flow import Flow
import os
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build  # ✅ Import this
from google.oauth2.credentials import credentials  # ✅ Import this
from google_auth_oauthlib.flow import InstalledAppFlow



# Allow HTTP for local development
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

GOOGLE_CLIENT_SECRET_FILE = os.getenv("GOOGLE_CREDENTIALS_PATH", "/Users/mihirmistry/secrets/client_secret.json")
REDIRECT_URI = "http://localhost:8000/google/callback"

def google_login(request):
    """Generate Google login URL."""
    flow = Flow.from_client_secrets_file(
        GOOGLE_CLIENT_SECRET_FILE,
        scopes=["openid", "email", "profile"],
        redirect_uri=REDIRECT_URI
    )
    auth_url, _ = flow.authorization_url(prompt="consent")
    print(f"🔍 Google Login URL: {auth_url}")  # Debugging print

    return JsonResponse({'auth_url': auth_url})

def google_callback(request):
    flow = Flow.from_client_secrets_file(
        GOOGLE_CLIENT_SECRET_FILE,
        scopes=["openid", "email", "profile", "https://www.googleapis.com/auth/drive.file"],
        redirect_uri="http://localhost:8000/google/callback"
        
    )
    
    flow.fetch_token(authorization_response=request.get_full_path())
    credentials = flow.credentials

    # 🔹 Store credentials in session
    request.session['google_credentials'] = json.dumps({
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    })

    # 🔹 Get user info
    service = build('oauth2', 'v2', credentials=credentials)
    user_info = service.userinfo().get().execute()

    return JsonResponse({
        "email": user_info["email"],
        "name": user_info["name"],
        "picture": user_info["picture"]
    })
def upload_to_drive(request):
    CLIENT_SECRET_FILE = "client_secret.json"
    SCOPES = ["https://www.googleapis.com/auth/drive.file"]

    # Run OAuth flow to get credentials dynamically
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    creds = flow.run_local_server(port=8080)  # Opens browser for authentication

    # Build Google Drive service
    drive_service = build('drive', 'v3', credentials=creds)

    # File metadata
    file_metadata = {'name': 'test_file.txt'}
    media = MediaFileUpload('test_file.txt', mimetype='text/plain')

    # Upload file
    file = drive_service.files().create(body=file_metadata, media_body=media).execute()

    return JsonResponse({'file_id': file.get('id')})

def fetch_drive_files(request):
    drive_service = build('drive', 'v3', credentials=credentials)
    results = drive_service.files().list(pageSize=10).execute()
    return JsonResponse({'files': results.get('files', [])})

