from app.services.google_drive import GoogleDriveService


drive = GoogleDriveService()


file = drive.upload_file(
    file_path="test.txt",
    file_name="test.txt",
    mime_type="text/plain"
)


print(file)