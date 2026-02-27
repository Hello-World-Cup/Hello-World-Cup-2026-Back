import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class GmailSmtpSender:
    def __init__(self) -> None:
        self.host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        self.port = int(os.getenv("SMTP_PORT", "587"))
        self.user = os.getenv("SMTP_USER")
        self.password = os.getenv("SMTP_PASSWORD")
        self.from_email = os.getenv("SMTP_FROM_EMAIL", self.user)
        self.from_name = os.getenv("SMTP_FROM_NAME", "HWC")

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