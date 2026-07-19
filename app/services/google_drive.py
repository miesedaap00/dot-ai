import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


SCOPES = [
    "https://www.googleapis.com/auth/drive.file"
]


class GoogleDriveService:

    def __init__(self):

        self.creds = None

        if os.path.exists("token.json"):

            self.creds = Credentials.from_authorized_user_file(
                "token.json",
                SCOPES
            )

        if self.creds and self.creds.expired and self.creds.refresh_token:

            self.creds.refresh(Request())

        elif not self.creds or not self.creds.valid:

            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES
            )

            self.creds = flow.run_local_server(
                port=0
            )

            with open("token.json", "w") as token:

                token.write(
                    self.creds.to_json()
                )

        self.service = build(
            "drive",
            "v3",
            credentials=self.creds
        )


    def upload_file(
        self,
        file_path,
        file_name,
        mime_type
    ):

        file_metadata = {
            "name": file_name
        }

        media = MediaFileUpload(
            file_path,
            mimetype=mime_type,
            resumable=True
        )

        uploaded_file = self.service.files().create(

            body=file_metadata,

            media_body=media,

            fields="id, name, mimeType, webViewLink"

        ).execute()

        return uploaded_file