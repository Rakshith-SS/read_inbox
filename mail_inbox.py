from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path
import json

from helpers import convert_datetime
from crud import save_to_inbox, filter_condition
from typing import Dict


class MailInbox():
    def __init__(self):
        self.SCOPES = [
            'https://www.googleapis.com/auth/gmail.readonly',
            'https://www.googleapis.com/auth/gmail.modify'
        ]

    def authorize(self) -> str:
        """
            Authenticate with google and save
            tokens in a python object form,
            to a file called token.pickle,
        """
        creds = None

        # The file token.pickle contains the user access token.
        # Check if it exists
        if os.path.exists('token.pickle'):

            # Read the token from the file and store it in the variable creds
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

        # If credentials are not available or are invalid,
        # ask the user to log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)

            # Save the access token in token.pickle file for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        return creds

    def read_inbox(self) -> None:
        """
            Read the inbox of the authenticated user and
            save to the database
        """
        creds = self.authorize()
        service = build('gmail', 'v1', credentials=creds)
        result = service.users().messages().list(userId='me').execute()
        messages = result.get('messages')
        txt = service.users().messages().get(
            userId='me', id=messages[0]["id"]).execute()
        for msg in messages:
            txt = service.users().messages().get(
                userId='me', id=msg['id']).execute()
            try:
                # Get value of 'payload' from dictionary 'txt'
                save_detail = {}
                payload = txt['payload']
                headers = payload['headers']
                parts = payload['parts']
                part = [part for part in parts if part.get(
                    'mimeType') == 'text/html'][0]
                content_header = [header for header in part[
                    'headers'] if header['name'] == 'Content-Type'][0]

                save_detail["mime_type"] = part.get('mimeType')
                save_detail["body"] = part.get('body').get('data')
                save_detail["content_type"] = content_header.get('value')
                save_detail["msg_id"] = msg['id']

                for data in headers:
                    if data["name"] in ["Subject", "From", "Date", "To"]:
                        if data["name"] == "Date":
                            save_detail[data["name"]] = convert_datetime(
                                data["value"])
                        else:
                            save_detail[data["name"]] = data["value"]
                save_to_inbox(**save_detail)
            except KeyError:
                pass

    def load_rules(self) -> Dict:
        """
            Load all the rules from
            rules.json file
        """
        with open('rules.json', 'r') as file:
            rules = json.load(file)
        return rules

    def process_emails(self) -> None:
        """
            read emails from the database, process
            them based on a set of rules.
        """
        rules = self.load_rules()
        creds = self.authorize()
        service = build('gmail', 'v1', credentials=creds)
        all_conditon = rules["all"]
        any_condition = rules["any"]

        for data in all_conditon:
            mails = filter_condition(rule='all', **data)
            for mail in mails:
                msg_id = mail.msg_id
                service.users().messages().modify(
                    userId='me',
                    id=msg_id,
                    body={
                        "addLabelIds": [
                            "Label_8011922581381469318"
                        ],
                        "removeLabelIds": [
                            "UNREAD"
                        ]
                    }
                ).execute()

        for data in any_condition:
            mails = filter_condition(**data)
            for mail in mails:
                msg_id = mail.msg_id
                service.users().messages().modify(
                    userId='me',
                    id=msg_id,
                    body={
                        "addLabelIds": [
                            "Label_8011922581381469318"
                        ],
                        "removeLabelIds": [
                            "UNREAD"
                        ]
                    }
                ).execute()
