import os

class Config:
    # Base paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    CONFIG_DIR = os.path.join(BASE_DIR, 'config')
    STORAGE_DIR = os.path.join(BASE_DIR, 'storage/invoices')

    # Google API configurations
    SERVICE_ACCOUNT_FILE = os.path.join(CONFIG_DIR, 'service_account.example.json')
    GOOGLE_SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive.readonly'
    ]
    SPREADSHEET_ID = 'your-spreadsheet-id-here'

    # Gmail configurations
    GMAIL_CREDENTIALS_FILE = os.path.join(CONFIG_DIR, 'gmail_credentials.example.json')
    GMAIL_SCOPES = ['https://www.googleapis.com/auth/gmail.send']
    GMAIL_TOKEN_FILE = os.path.join(CONFIG_DIR, 'token.pickle')

    @classmethod
    def init_directories(cls):
        """Create necessary directories if they don't exist"""
        os.makedirs(cls.STORAGE_DIR, exist_ok=True) 