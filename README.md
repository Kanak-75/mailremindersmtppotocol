# Email Sender using Python and SMTP (Gmail-ready)

This Python script sends an email using SMTP (defaults to Gmail). Configuration is loaded from environment variables (via `.env`).

## Prerequisites

1. Python 3.x
2. Dependencies:

    ```bash
    pip install python-dotenv
    ```

## Setup

1. Copy `example.env` to `.env` and fill in values:

    ```plaintext
    EMAIL_SENDER=your_email@example.com
    EMAIL_PASSWORD=your_app_password_or_email_password
    EMAIL_RECEIVER=receiver@example.com
    
    # Optional SMTP configuration
    SMTP_HOST=smtp.gmail.com
    SMTP_USE_SSL=true
    SMTP_USE_STARTTLS=false
    SMTP_PORT=
    SMTP_TIMEOUT_SECONDS=30
    
    # Optional message content
    EMAIL_SUBJECT=Don't miss this email
    EMAIL_BODY=Please read the details here
    ```

2. For Gmail accounts, generate an App Password (recommended):
   - Enable 2-Step Verification in your Google account.
   - Create an App Password for "Mail" on your device.
   - Use that value for `EMAIL_PASSWORD`.

## Running

```bash
python email_sender.py
```

## What the script does

- Loads env vars using `python-dotenv`.
- Validates required vars: `EMAIL_SENDER`, `EMAIL_PASSWORD`, `EMAIL_RECEIVER`.
- Builds the email using `EmailMessage`.
- Connects via SSL on 465 by default. If `SMTP_USE_SSL=false` and `SMTP_USE_STARTTLS=true`, it uses STARTTLS (587 default).
- Handles authentication and SMTP errors with clear messages.

## Notes

- If you are not using Gmail, set `SMTP_HOST` and `SMTP_PORT` accordingly and choose SSL or STARTTLS per your provider.
- `.gitignore` is configured to exclude `.env` and Python cache files.
