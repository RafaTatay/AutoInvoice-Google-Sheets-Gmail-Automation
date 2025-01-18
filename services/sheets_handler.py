from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from datetime import datetime
import os
from typing import Dict, List
import io
from services.email_sender import EmailSender
from config.config import Config

class SheetsHandler:
    def __init__(self):
        # Setup credentials
        self.SERVICE_ACCOUNT_FILE = Config.SERVICE_ACCOUNT_FILE
        self.SCOPES = Config.GOOGLE_SCOPES
        self.SPREADSHEET_ID = Config.SPREADSHEET_ID
        self.STORAGE_DIR = Config.STORAGE_DIR
        
        # Initialize email sender
        self.email_sender = EmailSender()

        # Load credentials
        creds = Credentials.from_service_account_file(
            self.SERVICE_ACCOUNT_FILE, 
            scopes=self.SCOPES
        )
        
        # Build services
        self.sheets_service = build('sheets', 'v4', credentials=creds)
        self.drive_service = build('drive', 'v3', credentials=creds)

    def export_and_email_pdf(self, recipient_email: str) -> Dict[str, any]:
        """Exports the sheet as PDF and sends it via email"""
        try:
            # First export the PDF
            export_result = self.export_to_pdf()
            
            # Read the PDF file
            with open(export_result['filepath'], 'rb') as f:
                pdf_content = f.read()
            
            # Send via email
            self.email_sender.send_pdf_by_email(
                recipient_email=recipient_email,
                pdf_buffer=pdf_content,
                filename=export_result['filename']
            )
            
            return {
                "success": True,
                "filename": export_result['filename'],
                "filepath": export_result['filepath'],
                "email_sent": True,
                "recipient": recipient_email
            }
        except Exception as e:
            raise Exception(f"Error in export and email process: {str(e)}")

    def export_to_pdf(self) -> Dict[str, str]:
        """Exports the sheet as PDF with the format YYYY_MM.pdf"""
        try:
            current_date = datetime.now()
            filename = f"{current_date.strftime('%Y_%m')}.pdf"
            filepath = os.path.join(self.STORAGE_DIR, filename)

            # Export the spreadsheet as PDF
            request = self.drive_service.files().export_media(
                fileId=self.SPREADSHEET_ID,
                mimeType='application/pdf'
            )
            
            # Download the PDF
            pdf_content = request.execute()
            
            # Save to file
            with open(filepath, 'wb') as f:
                f.write(pdf_content)
            
            return {
                "success": True,
                "filename": filename,
                "filepath": filepath
            }
        except Exception as e:
            raise Exception(f"Error exporting PDF: {str(e)}")

    def update_dates(self) -> Dict[str, bool]:
        """Updates the dates in the sheet with current date in specified formats"""
        try:
            # Get current date in required formats
            current_date = datetime.now()
            date_dd_mm_yyyy = current_date.strftime("%d/%m/%Y")
            date_t_yyyy_mm = f"T-{current_date.strftime('%Y-%m')}"
            
            # Get first sheet
            sheet_name = self.get_sheets_list()[0]
            
            # Update date in C9
            self.modify_rows(
                f"{sheet_name}!C9",
                [[date_dd_mm_yyyy]]
            )
            
            # Update format in F12
            self.modify_rows(
                f"{sheet_name}!F12",
                [[date_t_yyyy_mm]]
            )
            
            return {
                "success": True,
                "date_updated": date_dd_mm_yyyy,
                "format_updated": date_t_yyyy_mm
            }
        except Exception as e:
            raise Exception(f"Error updating dates: {str(e)}")

    def modify_rows(self, range_name: str, values: List[List[str]]) -> Dict[str, any]:
        try:
            body = {
                'values': values
            }
            result = self.sheets_service.spreadsheets().values().update(
                spreadsheetId=self.SPREADSHEET_ID,
                range=range_name,
                valueInputOption='USER_ENTERED',
                body=body
            ).execute()
            return result
        except Exception as e:
            raise Exception(f"Error modifying rows: {str(e)}")

    def get_sheets_list(self) -> List[str]:
        try:
            metadata = self.sheets_service.spreadsheets().get(
                spreadsheetId=self.SPREADSHEET_ID
            ).execute()
            return [sheet['properties']['title'] for sheet in metadata.get('sheets', [])]
        except Exception as e:
            raise Exception(f"Error getting sheets list: {str(e)}") 