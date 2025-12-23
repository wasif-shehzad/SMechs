import smtplib
from sqlalchemy.orm import Session
from email.message import EmailMessage
from sqlalchemy.orm import Session
from app.schemas.email import SendEmailRequest


SMTP_HOST = "mail.smtp2go.com"
SMTP_PORT = 465  # SSL
SENDER_EMAIL = "tayyub.rafique@dmechs.com"  # Must be verified in SMTP2GO
SMTP_USERNAME = "Tayyub rafique"
SMTP_PASSWORD = "Tayyub@12345"

class EmailService:
    def __init__(self, db: Session):
        self.db = db
    def send_email(self, email_data: SendEmailRequest):
        msg = EmailMessage()
        msg["Subject"] = email_data.subject
        msg["From"] = SENDER_EMAIL
        msg["To"] = ", ".join(email_data.to)

        if email_data.cc:
            msg["Cc"] = ", ".join(email_data.cc)
        if email_data.bcc:
            msg["Bcc"] = ", ".join(email_data.bcc)

        if email_data.is_html:
            msg.set_content(email_data.body, subtype="html")
        else:
            msg.set_content(email_data.body)

        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as smtp:
            smtp.login(SENDER_EMAIL, SMTP_PASSWORD)
            smtp.send_message(msg)

email_crud = EmailService()

