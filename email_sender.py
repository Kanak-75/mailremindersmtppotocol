from email.message import EmailMessage
from dotenv import load_dotenv
import os
import ssl
import smtplib
from typing import Optional

# Load environment variables from .env
load_dotenv()


def get_bool_env(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def get_int_env(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def main() -> None:
    # Required credentials/addresses
    email_sender: str = require_env("EMAIL_SENDER")
    email_password: str = require_env("EMAIL_PASSWORD")
    email_receiver: str = require_env("EMAIL_RECEIVER")

    # Optional message fields
    subject: str = os.getenv("EMAIL_SUBJECT", "Don't miss this email")
    body: str = os.getenv("EMAIL_BODY", "Please read the details here")

    # SMTP configuration (with sensible defaults for Gmail)
    smtp_host: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    use_ssl: bool = get_bool_env("SMTP_USE_SSL", True)
    use_starttls: bool = get_bool_env("SMTP_USE_STARTTLS", not use_ssl)
    # Default ports: 465 for SSL, 587 for STARTTLS, fallback 25
    default_port = 465 if use_ssl else 587 if use_starttls else 25
    smtp_port: int = get_int_env("SMTP_PORT", default_port)
    timeout_seconds: int = get_int_env("SMTP_TIMEOUT_SECONDS", 30)

    # Compose message
    message = EmailMessage()
    message['From'] = email_sender
    message['To'] = email_receiver
    message['Subject'] = subject
    message.set_content(body)

    # Create SSL Context for secure communication
    context = ssl.create_default_context()

    try:
        if use_ssl:
            with smtplib.SMTP_SSL(smtp_host, smtp_port, context=context, timeout=timeout_seconds) as smtp:
                smtp.login(email_sender, email_password)
                smtp.send_message(message)
        else:
            with smtplib.SMTP(smtp_host, smtp_port, timeout=timeout_seconds) as smtp:
                # Advertise and upgrade the connection if STARTTLS is requested
                if use_starttls:
                    smtp.ehlo()
                    smtp.starttls(context=context)
                    smtp.ehlo()
                smtp.login(email_sender, email_password)
                smtp.send_message(message)
        print("Email sent successfully.")
    except smtplib.SMTPAuthenticationError as e:
        print("Authentication failed. Check EMAIL_SENDER and EMAIL_PASSWORD (use an App Password for Gmail).")
        raise
    except smtplib.SMTPException as e:
        print(f"SMTP error occurred: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise


if __name__ == "__main__":
    main()
 