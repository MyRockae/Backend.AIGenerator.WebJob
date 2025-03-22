import os
import tempfile
import ftplib
from django.conf import settings

def ftp_upload(server, username, password, local_file_path, remote_filename, port=21):
    session = None
    try:
        session = ftplib.FTP()
        session.connect(server, port)
        session.login(username, password)
        with open(local_file_path, 'rb') as file:
            session.storbinary(f'STOR {remote_filename}', file)
    finally:
        if session:
            session.quit()

def upload_profile_photo(request):
    # Ensure a file was provided.
    if 'photo' in request.data:
        uploaded_file = request.data['photo']
        # Use the user ID if authenticated; otherwise, use "anonymous".
        user_id = request.user.id if request.user.is_authenticated else "anonymous"
        remote_filename = f'users/{user_id}/profile_photo/{uploaded_file.name}'

        try:
            # Save the uploaded file to a temporary file.
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                for chunk in uploaded_file.chunks():
                    tmp.write(chunk)
                tmp_path = tmp.name
        except Exception:
            return None

    try:
        # Upload the temporary file to your FTP server.
        ftp_upload(
            server=settings.FTP_HOST,         # e.g., '141.136.43.220'
            username=settings.FTP_USER,         # e.g., 'u497284822.rockae.com'
            password=settings.FTP_PASSWORD,     # Your FTP password
            local_file_path=tmp_path,
            remote_filename=remote_filename,
            port=getattr(settings, 'FTP_PORT', 21)
        )
    except Exception:
        os.remove(tmp_path)
        return None

    # Remove the temporary file after uploading.
    os.remove(tmp_path)
    
    # Construct and return the public URL for the file.
    file_url = f"http://{settings.FTP_DOMAIN}/{remote_filename}"
    return file_url
