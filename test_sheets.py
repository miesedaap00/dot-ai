from app.services.google_sheets import GoogleSheetsService


sheets = GoogleSheetsService()


result = sheets.append_transaction(

    date="2026-07-19",

    merchant="Test Store",

    category="Testing",

    amount=50000,

    notes="Test dari Dot AI"

)


print(result)