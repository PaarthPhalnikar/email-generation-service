# send_email.py
import os
from typing import Optional
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content

from email_schemas import EmailResponse


SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")
DEFAULT_FROM_NAME = os.getenv("DEFAULT_FROM_NAME", "Email Bot")


if SENDGRID_API_KEY:
    sg_client = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
else:
    sg_client = None


def send_email_via_sendgrid(
    email: EmailResponse,
    to_email: str,
    to_name: Optional[str] = None,
) -> None:
    if not sg_client:
        raise RuntimeError("SENDGRID_API_KEY not set; cannot send email.")

    from_email = Email(DEFAULT_FROM_EMAIL, DEFAULT_FROM_NAME)
    to = To(to_email, to_name or to_email)
    content = Content("text/plain", email.body)

    mail = Mail(from_email, to, email.subject, content)
    response = sg_client.client.mail.send.post(request_body=mail.get())
    if response.status_code not in (200, 202):
        raise RuntimeError(f"SendGrid error: {response.status_code} {response.body}")
