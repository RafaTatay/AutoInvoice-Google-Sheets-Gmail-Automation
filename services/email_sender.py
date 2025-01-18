import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os
import pickle
from config.config import Config

class EmailSender:
    def __init__(self):
        self.SCOPES = Config.GMAIL_SCOPES
        self.credentials_path = Config.GMAIL_CREDENTIALS_FILE
        self.token_path = Config.GMAIL_TOKEN_FILE
        self.creds = self._get_credentials()
        self.service = build('gmail', 'v1', credentials=self.creds)

    def _get_credentials(self):
        """Gets valid user credentials from storage or creates new ones."""
        creds = None
        
        # The file token.pickle stores the user's access and refresh tokens
        if os.path.exists(self.token_path):
            with open(self.token_path, 'rb') as token:
                creds = pickle.load(token)
                
        # If there are no (valid) credentials available, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.token_path, 'wb') as token:
                pickle.dump(creds, token)
        return creds

    def send_pdf_by_email(self, recipient_emails: list[str], pdf_buffer: bytes, 
                         filename: str = "report.pdf") -> dict:
        try:
            # Convert single email to list if string is provided
            if isinstance(recipient_emails, str):
                recipient_emails = [recipient_emails]
            
            message = MIMEMultipart()
            message['To'] = ', '.join(recipient_emails)  # Join all emails with comma
            message['Subject'] = "Example Subject"

            # Add body text
            body = f"Please find attached the invoice ({filename})."
            message.attach(MIMEText(body, 'plain'))

            # Attach PDF
            pdf_attachment = MIMEApplication(pdf_buffer, _subtype="pdf")
            pdf_attachment.add_header('Content-Disposition', 'attachment', 
                                    filename=filename)
            message.attach(pdf_attachment)

            # Encode the message
            raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
            
            # Send the email
            try:
                message = (self.service.users().messages().send(
                    userId="me",
                    body={'raw': raw}
                ).execute())
                print(f'Message Id: {message["id"]}')
                return {
                    "success": True,
                    "message_id": message["id"],
                    "recipients": recipient_emails
                }
            except Exception as error:
                print(f'An error occurred: {error}')
                return {
                    "success": False,
                    "error": str(error)
                }

        except Exception as e:
            raise Exception(f"Error preparing email: {str(e)}") 