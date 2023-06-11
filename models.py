from sqlalchemy import Column, Integer, String, Text, DateTime
from database import Base
from sqlalchemy.sql import func


class MailInbox(Base):
    __tablename__ = 'mails'

    id = Column(Integer, primary_key=True)
    msg_id = Column(String(128), unique=True)
    sender = Column(Text)
    reciever = Column(Text)
    date_received = Column(DateTime(timezone=True))
    subject = Column(String(1024))
    body = Column(Text)
    content_type = Column(String(128))
    mime_type = Column(String(128))
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(),
                        onupdate=func.now())
