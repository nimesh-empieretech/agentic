import smtplib
import requests
from email.mime.text import MIMEText
from app.config import settings


def send_email_notification(to_email: str, subject: str, body: str):
    if not to_email or not settings.SMTP_HOST:
        return False
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = settings.MAIL_FROM
    msg["To"] = to_email

    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.sendmail(settings.MAIL_FROM, [to_email], msg.as_string())
    return True


def send_whatsapp_notification(phone: str, message: str):
    if not phone or not settings.WHATSAPP_API_URL:
        return False
    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_API_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {"phone": phone, "message": message}
    response = requests.post(
        settings.WHATSAPP_API_URL, json=payload, headers=headers, timeout=20
    )
    return response.ok
