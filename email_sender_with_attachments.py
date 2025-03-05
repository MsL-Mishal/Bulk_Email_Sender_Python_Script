import smtplib
import time
import pandas as pd
import random
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get credentials securely from environment variables
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

# File paths
ATTACHMENTS_FOLDER = os.getenv("ATTACHMENTS_FOLDER", "attachments/")

# Email Subject
EMAIL_SUBJECT = "Welcome to Our Platform!"

# Main Email Body Template
EMAIL_BODY_TEMPLATE = """
Dear {username},

Thank you for joining us! We are excited to have you on board.

We look forward to working with you and hope you have a great experience.

Best Regards,
"""

# Email Signature
EMAIL_SIGNATURE = """
{sender_name}
{sender_designation}
{organization_name}
"""

# Final Email Template (Combining Both)
EMAIL_TEMPLATE = EMAIL_BODY_TEMPLATE + EMAIL_SIGNATURE

# Read user data from Excel file
file_path = "email_list_with_attachments.xlsx"
df = pd.read_excel(file_path)

# Define batch settings
BATCH_SIZE = 100  # Emails per batch
DELAY_BETWEEN_EMAILS = random.randint(20, 60)  # Random delay between emails
DELAY_BETWEEN_BATCHES = 900  # 15 minutes delay after each batch

# Email sender details (modify if needed)
SENDER_NAME = "John Doe"
SENDER_DESIGNATION = "HR Manager"
ORGANIZATION_NAME = "ABC Corp"

def send_email(recipient_email, recipient_name, attachment_filename=None):
    try:
        # Set up SMTP server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)

        # Create email message
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = recipient_email
        msg["Subject"] = EMAIL_SUBJECT

        # Customize email content
        email_body = EMAIL_TEMPLATE.format(
            username=recipient_name,
            sender_name=SENDER_NAME,
            sender_designation=SENDER_DESIGNATION,
            organization_name=ORGANIZATION_NAME
        )
        msg.attach(MIMEText(email_body, "plain"))

        # Attach file if provided
        if attachment_filename:
            attachment_path = os.path.join(ATTACHMENTS_FOLDER, attachment_filename)
            if os.path.exists(attachment_path):
                with open(attachment_path, "rb") as attachment:
                    mime_base = MIMEBase("application", "octet-stream")
                    mime_base.set_payload(attachment.read())
                    encoders.encode_base64(mime_base)
                    mime_base.add_header(
                        "Content-Disposition", f"attachment; filename={attachment_filename}"
                    )
                    msg.attach(mime_base)

        # Send email
        server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())
        server.quit()

        print(f"Email sent successfully to {recipient_name} ({recipient_email})")

    except Exception as e:
        print(f"Failed to send email to {recipient_name} ({recipient_email}): {e}")

# Process emails in batches
for i in range(0, len(df), BATCH_SIZE):
    batch = df.iloc[i : i + BATCH_SIZE]
    
    for index, row in batch.iterrows():
        attachment_filename = row["Attachment"] if "Attachment" in df.columns and pd.notna(row["Attachment"]) else None
        send_email(row["Email"], row["Username"], attachment_filename)
        time.sleep(DELAY_BETWEEN_EMAILS)  # Wait before sending next email

    print(f"Batch {i // BATCH_SIZE + 1} completed. Waiting {DELAY_BETWEEN_BATCHES / 60} minutes before next batch...")
    time.sleep(DELAY_BETWEEN_BATCHES)  # Pause between batches
