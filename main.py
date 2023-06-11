from database import Base, engine
from mail_inbox import MailInbox


def main():
    Base.metadata.create_all(engine)
    mail = MailInbox()
    mail.read_inbox()


if __name__ == "__main__":
    main()
