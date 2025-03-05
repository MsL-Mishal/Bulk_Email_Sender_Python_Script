import smtplib #for sending emails
import time #for delay between emails
import pandas as pd #for reading Excel file
import random #for generating random delay between emails
import os #for environment variables
from email.mime.multipart import MIMEMultipart #this is used to send email with attachments
from email.mime.text import MIMEText #this is used to send email with text
from dotenv import load_dotenv  #for loading environment variables

# Load environment variables from .env file
load_dotenv()

# Debugging - Print to check if values are loaded
print(f"SENDER_EMAIL: {os.getenv('SENDER_EMAIL')}")
print(f"APP_PASSWORD: {os.getenv('APP_PASSWORD')}")

# Get credentials from environment variables
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")

# SMTP Configuration
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

# Email Content Template
EMAIL_SUBJECT = "Welcome to Our Platform!"
EMAIL_TEMPLATE = """
Dear {username},

Thank you for joining us! We are excited to have you on board.

Best Regards,  
Your Company
"""

# Read email list from Excel file
file_path = "email_list.xlsx"
df = pd.read_excel(file_path)

# Define batch settings
BATCH_SIZE = 100  # Number of emails per batch
DELAY_BETWEEN_EMAILS = random.randint(20, 60)  # Random delay between emails (in seconds)
DELAY_BETWEEN_BATCHES = 900  # Wait 15 minutes after each batch

def send_email(recipient_email, recipient_name):
    try:
        # Set up the email server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT) # Create an SMTP object
        server.starttls() # Enable TLS which is required by Gmail to send emails. TLS stands for Transport Layer Security. It is a protocol that provides privacy and data integrity between two communicating applications. This command will encrypt the email and password
        server.login(SENDER_EMAIL, APP_PASSWORD) # Login to your email account

        # Create the email
        msg = MIMEMultipart() # Create a message object
        msg["From"] = SENDER_EMAIL # Set the sender's email address
        msg["To"] = recipient_email # Set the recipient's email address
        msg["Subject"] = EMAIL_SUBJECT # Set the email subject

        # Customize email content
        email_body = EMAIL_TEMPLATE.format(username=recipient_name) # Fill in the email template with user-specific content
        msg.attach(MIMEText(email_body, "plain")) # Attach the email body as plain text

        # Send email
        server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string()) # Send the email as a string
        server.quit() # Disconnect from the server

        print(f"Email sent successfully to {recipient_name} ({recipient_email})")

    except Exception as e:
        print(f"Failed to send email to {recipient_name} ({recipient_email}): {e}")

# Process emails in batches
for i in range(0, len(df), BATCH_SIZE):
    batch = df.iloc[i : i + BATCH_SIZE] # Get a batch of emails that corresponds to the current index range
    
    for index, row in batch.iterrows():
        send_email(row["Email"], row["Username"]) # Send email to each recipient
        time.sleep(DELAY_BETWEEN_EMAILS)  # Wait before sending the next email

    print(f"Batch {i // BATCH_SIZE + 1} completed. Waiting {DELAY_BETWEEN_BATCHES / 60} minutes before next batch...")
    time.sleep(DELAY_BETWEEN_BATCHES)  # Pause between batches
