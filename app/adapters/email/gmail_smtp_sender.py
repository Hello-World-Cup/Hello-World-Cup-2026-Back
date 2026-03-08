import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.domain.config import settings
from app.ports.driven.email.email_sender_interface import EmailSenderInterface

class GmailSmtpSender(EmailSenderInterface):
    def __init__(self) -> None:
        self.host = settings.SMTP_HOST
        self.port = settings.SMTP_PORT
        self.user = settings.SMTP_USER
        self.password = settings.SMTP_PASSWORD
        self.from_email = settings.SMTP_FROM_EMAIL or self.user
        self.from_name = settings.SMTP_FROM_NAME

        if not self.user or not self.password or not self.from_email:
            raise RuntimeError("SMTP_USER / SMTP_PASSWORD / SMTP_FROM_EMAIL are required")

    def send_verification_email(self, to_email: str, user_name: str, verify_link: str) -> None:
        subject = "Verify your email"
        body = (
            f"Hi {user_name},\n\n"
            f"Please verify your email by clicking this link:\n{verify_link}\n\n"
            f"If you didn’t request this, ignore this email."
        )

        msg = MIMEMultipart()
        msg["From"] = f"{self.from_name} <{self.from_email}>"
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(self.host, self.port) as server:
            server.starttls()
            server.login(self.user, self.password)
            server.sendmail(self.from_email, to_email, msg.as_string())