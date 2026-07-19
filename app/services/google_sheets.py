from googleapiclient.discovery import build

from app.config import config

from app.services.google_drive import GoogleDriveService


class GoogleSheetsService:

    def __init__(self):

        drive_service = GoogleDriveService()


        self.service = build(

            "sheets",

            "v4",

            credentials=drive_service.creds

        )


        self.spreadsheet_id = (
            config.GOOGLE_SHEETS_ID
        )


        if not self.spreadsheet_id:

            raise ValueError(
                "GOOGLE_SHEETS_ID belum ditemukan di .env"
            )


    def append_transaction(

        self,

        date,

        merchant,

        category,

        amount,

        notes

    ):

        values = [[

            date,

            merchant,

            category,

            amount,

            notes

        ]]


        body = {

            "values": values

        }


        result = (

            self.service

            .spreadsheets()

            .values()

            .append(

                spreadsheetId=self.spreadsheet_id,

                range="Sheet1!A:E",

                valueInputOption="USER_ENTERED",

                insertDataOption="INSERT_ROWS",

                body=body

            )

            .execute()

        )


        return result