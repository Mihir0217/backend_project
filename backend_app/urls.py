from django.urls import path
from .views import fetch_drive_files, google_login, google_callback, upload_to_drive

urlpatterns = [
    path('google/login/', google_login, name='google-login'),
    path('google/callback/', google_callback, name='google-callback'),
    path('drive/upload/', upload_to_drive, name='drive-upload'),
    path('drive/files/', fetch_drive_files, name='drive-files')
]



# from django.urls import path
# from .google_auth import google_login, google_callback

# urlpatterns = [
#     path('auth/login/', google_login, name='google_login'),
#     path('auth/callback/', google_callback, name='google_callback'),
# ]
