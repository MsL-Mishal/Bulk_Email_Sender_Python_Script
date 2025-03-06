import smtplib
import time
import pandas as pd
import random
import os
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from email import encoders
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

# Get credentials securely from environment variables
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

# File paths
ATTACHMENTS_FOLDER = os.getenv("ATTACHMENTS_FOLDER", "attachments/")

# Logging Configuration
LOG_FILE = os.getenv("LOG_FILE", "logs/email_log.txt")
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)  # Ensure logs directory exists

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


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

def attach_file(msg, attachment_filename):
    """Attach a file (PDF or Image) to the email."""
    attachment_path = os.path.join(ATTACHMENTS_FOLDER, attachment_filename)

    if os.path.exists(attachment_path):  # Ensure file exists
        mime_type, _ = mimetypes.guess_type(attachment_path)  # Detect file type
        with open(attachment_path, "rb") as attachment_file:
            if mime_type and mime_type.startswith("image"):  # Image file
                part = MIMEImage(attachment_file.read(), name=attachment_filename)
            elif mime_type == "application/pdf":  # PDF file
                part = MIMEApplication(attachment_file.read(), Name=attachment_filename)
                part["Content-Disposition"] = f'attachment; filename="{attachment_filename}"'
            else:  # Other unsupported file types
                print(f"Unsupported file type: {attachment_filename}")
                return

            msg.attach(part)
            print(f"Attached: {attachment_filename}")
    else:
        print(f"Warning: Attachment {attachment_filename} not found!")

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
        if attachment_filename and isinstance(attachment_filename, str) and attachment_filename.strip():
            attach_file(msg, attachment_filename.strip())

        # Send email
        server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())
        server.quit()

        success_message = f"Email sent successfully to {recipient_name} ({recipient_email})"
        print(success_message)
        logging.info(success_message)  # Log success

    except Exception as e:
        error_message = f"Failed to send email to {recipient_name} ({recipient_email}): {e}"
        print(error_message)
        logging.error(error_message)  # Log failure


# Process emails in batches
for i in range(0, len(df), BATCH_SIZE):
    batch = df.iloc[i : i + BATCH_SIZE]
    
    logging.info(f"Starting batch {i//BATCH_SIZE + 1} with {len(batch)} emails.")
    
    for index, row in batch.iterrows():
        attachment_filename = row["Attachment"] if "Attachment" in df.columns and pd.notna(row["Attachment"]) else None
        send_email(row["Email"], row["Username"], attachment_filename)
        
        time.sleep(DELAY_BETWEEN_EMAILS)  # Random delay

    logging.info(f"Completed batch {i//BATCH_SIZE + 1}. Waiting {DELAY_BETWEEN_BATCHES} seconds before next batch.")
    time.sleep(DELAY_BETWEEN_BATCHES)
