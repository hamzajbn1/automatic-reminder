import os
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from google_api import create_service



def init_gmail_service(client_file, api_name='gmail', api_version='v1', scopes=['https://mail.google.com/']):
    return create_service(client_file, api_name, api_version, scopes)

def create_draft_email(service, to, subject, body, body_type='plain', attachment_paths=None):
    message = MIMEMultipart()
    message['to'] = to # the email address of the person you are sending it to
    message['subject'] = subject # email headers.

    # Validate body type (must be 'plain' or 'html')
    if body_type.lower() not in ['plain', 'html']:
        raise ValueError("body_type must be either 'plain' or 'html'")

    # Attach the body text to the email
    message.attach(MIMEText(body, body_type.lower()))

    # Process attachments if any are provided
    if attachment_paths:
        # Each attachment_path represents one file.
        for attachment_path in attachment_paths:
            if os.path.exists(attachment_path):
                filename = os.path.basename(attachment_path)

                # Open the file in binary mode
                with open(attachment_path, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    # read the file then store it.
                    part.set_payload(attachment.read())

                encoders.encode_base64(part)

                # Add headers for the attachment
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename= {filename}",
                )

                message.attach(part)
            else:
                raise FileNotFoundError(f"File not found - {attachment_path}")

    # Convert the entire message to a URL-safe base64 string
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

    # Call the Gmail API to create the draft
    draft = service.users().drafts().create(
        userId='me',
        body={'message': {'raw': raw_message}}
    ).execute()

    return draft

def send_draft_email(service, draft_id):
    # The API call that triggers the send action. It only needs the id of the draft.
    draft = service.users().drafts().send(userId='me', body={'id': draft_id}).execute()
    return draft