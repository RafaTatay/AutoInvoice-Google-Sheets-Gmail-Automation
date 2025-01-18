# AutoInvoice Google Sheets & Gmail Automation

Automatically generates and emails invoices from Google Sheets using Gmail API.

## Prerequisites

Before you begin, you'll need:

- Python 3.8+
- A Google Cloud Platform account
- A Google Workspace account (for Gmail)
- A Google Sheet containing your invoice template

## Initial Setup

### 1. Google Cloud Platform Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable these APIs in "APIs & Services > Library":
   - Google Sheets API
   - Google Drive API
   - Gmail API

### 2. Credentials Setup

#### Service Account (for Sheets & Drive):

1. In Google Cloud Console:
   - Navigate to "IAM & Admin > Service Accounts"
   - Click "Create Service Account"
   - Name: "autoinvoice-sheets" (or your preference)
   - Create and download the JSON key
2. Save the downloaded JSON as: `config/service_account.json`
3. Share your Google Sheet with the service account email

#### Gmail OAuth2:

1. In Google Cloud Console:
   - Go to "APIs & Services > Credentials"
   - Create OAuth 2.0 Client ID (Desktop application)
   - Download the JSON
2. Save as: `config/gmail_credentials.json`

### 3. Local Setup

1. Clone and enter the repository:

```bash
git clone https://github.com/RafaTatay/AutoInvoice-Google-Sheets-Gmail-Automation.git
cd AutoInvoice-Google-Sheets-Gmail-Automation
```

2. Create virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up configuration files:

```bash
cp config/config.example.py config/config.py
cp config/service_account.example.json config/service_account.json
cp config/gmail_credentials.example.json config/gmail_credentials.json
```

5. Update `config/config.py` with your:
   - Spreadsheet ID (from Google Sheet URL)
   - Any other custom configurations
6. Update recipient email in `main.py`:
   - Open `main.py`
   - Locate `recipient_email = "example@gmail.com"`
   - Replace with your desired email address

## Usage

Run the script:

```bash
python main.py
```

On first run:

1. Browser will open for Gmail authorization
2. Login and grant permissions
3. Token will be saved as `token.pickle`

## Project Structure

```
.
├── config/
│   ├── config.py                               # Your configuration
│   ├── config.example.py                       # Example configuration
│   ├── service_account.json   # Sheets API credentials
│   ├── gmail_credentials.json   # Gmail API credentials
│   └── service_account.example.json            # Example service account
├── services/
│   ├── sheets_handler.py                       # Sheets operations
│   └── email_sender.py                         # Email operations
├── storage/
│   └── invoices/                              # Generated PDFs
└── main.py                                     # Entry point
```

## Expected Google Sheet Format

The script expects:

- Date field in cell C9
- Invoice number in cell F12 (format: T-YYYY-MM)

## Fields Modified by Script

The script automatically updates the following fields in your Google Sheet:

- **Date (Cell C9)**: Current date is inserted
- **Invoice Number (Cell F12)**: Auto-generated in format T-YYYY-MM

To modify which cells are updated:

1. Open `services/sheets_handler.py`
2. Modify the `update_date()` and `update_invoice_number()` functions
3. Update cell references as needed

## Security Notes

- Never commit credential files
- Keep `token.pickle` secure
- All sensitive files are in `.gitignore`
- Required credentials:
  - `service_account.json`
  - `gmail_credentials.json`
  - `token.pickle` (generated on first run)

## Troubleshooting

Common issues:

1. "Not authorized":

   - Check service account has access to Sheet
   - Verify APIs are enabled

2. "Token expired":

   - Delete `token.pickle`
   - Rerun for fresh authentication

3. "File not found":
   - Verify all credential files exist
   - Check file paths in `config.py`

## License

MIT License - See LICENSE file
