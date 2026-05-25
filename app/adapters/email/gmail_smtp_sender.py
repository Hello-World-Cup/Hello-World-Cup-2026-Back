import json
import urllib.request
import urllib.error
from app.domain.config import settings
from app.ports.driven.email.email_sender_interface import EmailSenderInterface

class GmailSmtpSender(EmailSenderInterface):
    def __init__(self) -> None:
        self.from_name = settings.SMTP_FROM_NAME or "Hello World Cup"
        self.google_script_url = settings.GOOGLE_SCRIPT_URL

    def send_verification_email(
        self, to_email: str, user_name: str, verify_link: str, temporary_password: str
    ) -> None:
        
        payload = {
            "to_email": to_email,
            "user_name": user_name,
            "verify_link": verify_link,
            "temporary_password": temporary_password,
            "from_name": self.from_name
        }
        
        data = json.dumps(payload).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        
        req = urllib.request.Request(self.google_script_url, data=data, headers=headers, method="POST")
        
        try:
            with urllib.request.urlopen(req) as _response:
                pass
        except urllib.error.URLError as e:
            raise RuntimeError(f"Failed to send email via Google Apps Script: {str(e)}")