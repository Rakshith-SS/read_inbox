import unittest
from mail_inbox import MailInbox
from googleapiclient.discovery import build
from crud import get_all_msg_ids


class TestMailInbox(unittest.TestCase):

    def test_read_inbox(self) -> bool:
        """
            check if the mails stored in database are valid.
        """
        mail = MailInbox()
        creds = mail.authorize()
        service = build('gmail', 'v1', credentials=creds)
        msg_ids = get_all_msg_ids()

        for msg_id in msg_ids:
            txt = service.users().messages().get(
                userId='me', id=msg_id).execute()
            self.assertTrue(msg_id == txt['id'], True)

    def test_process_mail(self) -> bool:
        """
            check if processed mails, are marked read.
        """
        mail = MailInbox()
        processed_msg_ids = mail.process_emails()
        creds = mail.authorize()
        service = build('gmail', 'v1', credentials=creds)

        for msg_id in processed_msg_ids:
            txt = service.users().messages().get(
                userId='me', id=msg_id).execute()
            self.assertTrue('UNREAD' not in txt['labelIds'], True)
        service.close()


if __name__ == '__main__':
    unittest.main()
