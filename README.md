# Orange Pill Invoice Generator

Automatically generates and emails invoices from Google Sheets.

## Setup

1. Clone the repository

```bash
git clone https://github.com/yourusername/orange-pill-invoice.git
cd orange-pill-invoice
```

2. Create and activate virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Set up configuration:

   - Copy `config/google_config.example.py` to `config/google_config.py`
   - Copy `config/gmail_credentials.example.json` to `config/gmail_credentials_learningheroes.json`
   - Create a Google Cloud Project and enable Gmail and Google Sheets APIs
   - Download service account key and save as `config/orange_pill_bill_service_account.json`
   - Update `google_config.py` with your Google Sheet ID

5. Run the script

```bash
python main.py
```

## Configuration

### Required Files

- `config/google_config.py`: Main configuration file
- `config/orange_pill_bill_service_account.json`: Service account credentials for Google Sheets
- `config/gmail_credentials_learningheroes.json`: OAuth2 credentials for Gmail

### Google Sheet Format

The script expects a Google Sheet with the following format:

- Date field in cell C9
- Invoice number in cell F12 (format: T-YYYY-MM)

## Features

- Updates dates automatically
- Exports sheet to PDF
- Sends PDF via email
- Stores PDFs locally in storage/invoices/

## License

MIT License
