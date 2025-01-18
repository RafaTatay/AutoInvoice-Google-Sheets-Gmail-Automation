from services.sheets_handler import SheetsHandler

def main():
    try:
        print("Starting Invoice Generation")
        
        # Initialize handler
        sheets = SheetsHandler()
        
        # Update dates in the sheet
        date_result = sheets.update_dates()
        print("\nDates updated:")
        print(f"- Date in C9: {date_result['date_updated']}")
        print(f"- Format in F12: {date_result['format_updated']}")
        
        # Export to PDF and send email
        recipient_email = "example@gmail.com"
        result = sheets.export_and_email_pdf(recipient_email)
        
        print(f"\nInvoice processed successfully:")
        print(f"- PDF saved as: {result['filename']}")
        print(f"- Location: {result['filepath']}")
        print(f"- Email sent to: {result['recipient']}")
        
        print("\nProcess completed successfully!")
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 