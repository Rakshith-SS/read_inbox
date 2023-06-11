from models import MailInbox
from database import SessionLocal


def save_to_inbox(**kwargs) -> None:
    """
        Connect to databse and save emails
    """

    db = SessionLocal()

    print(kwargs.get('Date'))

    mail_exists = db.query(MailInbox).filter_by(
        msg_id=kwargs.get('msg_id')).first()

    if mail_exists is None:
        mail_inbox = MailInbox()
        mail_inbox.msg_id = kwargs.get('msg_id')
        mail_inbox.sender = kwargs.get('From')
        mail_inbox.reciever = kwargs.get('To')
        mail_inbox.date_received = kwargs.get('Date')
        mail_inbox.subject = kwargs.get('Subject')
        mail_inbox.body = kwargs.get('body')
        mail_inbox.content_type = kwargs.get('content_type')
        mail_inbox.mime_type = kwargs.get('mime_type')

        db.add(mail_inbox)
        db.commit()
        db.close()
