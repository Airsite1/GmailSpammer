from __future__ import print_function
import base64
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
import os
from apiclient import errors
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
SCOPES=['https://www.googleapis.com/auth/gmail.compose']


def main():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('gmail', 'v1', credentials=creds)
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    for i in range(100):
        message =  create_message('me', 'EMAIL_HERE@gmail.com','THIS IS THE POWER OF CODING U SHOULDA BEEN A CS MAJOR', ':))')
        send_message(service, "me", message)
def send_message(service, user_id, message):
    message = (service.users().messages().send(userId=user_id, body=message).execute())
    print ('Message Id: %s' % message['id'])
    return message
def create_message(sender, to, subject, message_text):
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  message = base64.urlsafe_b64encode(message.as_bytes())
  raw = message.decode()
  return {'raw': raw}

if __name__ == '__main__':
    main()
