from models import MailInbox
from database import SessionLocal
from datetime import datetime, timedelta
from sqlalchemy import or_


def save_to_inbox(**kwargs) -> None:
    """
        Connect to databse and save emails
    """

    db = SessionLocal()

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


def filter_condition(rule=all, **kwargs) -> list[MailInbox]:
    sender_key = kwargs.get('From')
    subject_key = kwargs.get('Subject')
    date_key = kwargs.get('Date')

    db = SessionLocal()
    sender_query = filter_predicates(sender_key['predicate'],
                                     sender_key['field'],
                                     sender_key['value']
                                     )
    date_query = filter_predicates(date_key['predicate'],
                                   date_key['field'],
                                   date_key['value']
                                   )
    subject_query = filter_predicates(subject_key['predicate'],
                                      subject_key['field'],
                                      subject_key['value']
                                      )

    if rule == 'all':
        mails = db.query(MailInbox).filter(
            sender_query,
            subject_query,
            date_query
        ).all()
    else:
        mails = db.query(MailInbox).filter(
            or_(
                sender_query,
                subject_query,
                date_query
            )).all()

    return mails


def filter_predicates(predicate: str, field: str, value: str) -> MailInbox:
    if predicate == 'contains':
        if field == 'sender':
            query_string = MailInbox.sender.icontains(value)
        if field == 'subject':
            query_string = MailInbox.subject.icontains(value)

    if predicate == 'not equals':
        if field == 'sender':
            query_string = MailInbox.sender != value

        if field == 'subject':
            query_string = MailInbox.subject != value

    if field == 'date_received':
        current_time = datetime.now()
        days_ago = current_time - timedelta(days=value)

        query_string = MailInbox.date_received > days_ago

    return query_string
