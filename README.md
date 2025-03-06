# Bulk Email Sender with Optional Attachments

This project is a Python-based bulk email sender that allows sending personalized emails to multiple recipients. It supports email attachments, environment variable handling for sensitive credentials, and batch processing to prevent spam.

## 📌 Features

- Send bulk emails using SMTP.
- Secure credential management via `.env` file.
- Supports **both emails with and without attachments**.
- Reads recipient details from an Excel file (`email_list.xlsx`).
- Customizable email content.
- Batches emails to prevent spam issues.
- Supports multiple SMTP providers (Gmail, Outlook, etc.).
- Enhanced logging for debugging and tracking email status.
- Improved error handling and optimized email sending delays.

---

## 📂 Folder Structure

```
/bulk_email_sender
│── .gitignore                   # Prevents tracking sensitive files
│── .env                          # Stores environment variables (Not to be committed)
│── .env-example                  # Example environment variables file
│── requirements.txt               # Python dependencies
│── email_list.xlsx                # List of recipients (Without attachments)
│── email_list_with_attachments.xlsx # List of recipients with attachment filenames
│── attachments/                    # Folder containing email attachments
│   ├── sampledoc.pdf
│   ├── sampledoc1.pdf
│   ├── sampleimage1.jpg
│   ├── sampleimage2.jpg
│   ├── sampleimage3.jpg
│── email_sender.py                 # Script for sending emails without attachments
│── email_sender_with_attachments.py # Script for sending emails with attachments
│── logs/                            # Folder to store email logs
│   ├── email_log.txt                # Log file for tracking sent emails
│── README.md                        # Project documentation
```

---

## 🛠️ Setup Instructions

### 1️⃣ **Clone the Repository**

```bash
git clone https://github.com/MsL-Mishal/Bulk_Email_Sender_Python_Script.git
cd Bulk_Email_Sender_Python_Script
```

### 2️⃣ **Create and Activate Virtual Environment**

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3️⃣ **Install Dependencies**

```bash
pip install -r requirements.txt
```

### 4️⃣ **Set Up Environment Variables**

- Create a `.env` file in the root directory.
- Copy contents from `.env-example` and replace placeholders with actual values.

Example `.env` file:

```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your_email@gmail.com
APP_PASSWORD=your_app_password
ATTACHMENTS_FOLDER=attachments/
LOG_FILE=logs/email_log.txt
```

**🚨 Important:**

- Never commit the `.env` file to GitHub!
- `.gitignore` already includes `.env`, preventing accidental commits.

---

## 📄 **Preparing the Recipient List**

### **1️⃣ Email List Without Attachments**

The `email_list.xlsx` file should have the following columns:

| Username   | Email                                            |
| ---------- | ------------------------------------------------ |
| Mishal K R | [mishal@example.com](mailto\:mishal@example.com) |
| Alice      | [alice@example.com](mailto\:alice@example.com)   |
| Bob        | [bob@example.com](mailto\:bob@example.com)       |

### **2️⃣ Email List With Attachments**

If sending attachments, use `email_list_with_attachments.xlsx`:

| Username   | Email                                              | Attachment       |
| ---------- | -------------------------------------------------- | ---------------- |
| Mishal K R | [mishal@example.com](mailto\:mishal@example.com)   | sampledoc.pdf    |
| Alice      | [alice@example.com](mailto\:alice@example.com)     | sampledoc1.pdf   |
| Bob        | [bob@example.com](mailto\:bob@example.com)         | sampleimage1.jpg |

Ensure that **all attachment files are inside the ****`attachments/`**** folder**.

---

## 📧 **Sending Emails**

### **1️⃣ Sending Emails Without Attachments**

Run:

```bash
python email_sender.py
```

### **2️⃣ Sending Emails With Attachments**

Run:

```bash
python email_sender_with_attachments.py
```

---

## 🔄 **Batch Processing to Prevent Spam**

- **Emails are sent in batches** (default: 100 per batch).
- **Random delay** (20-60 sec) between each email.
- **15-minute cooldown** between batches.
- Modify these values inside the script if needed.

---

## 📜 **Logging and Error Handling**

- Email sending status is logged in `logs/email_log.txt`.
- Errors and failed email deliveries are also recorded.
- Improved handling of SMTP errors and connection issues.

---

## 🚀 **Deploying or Scheduling Emails**

If you need to **automate the script**, you can use:

- **Windows Task Scheduler** (Windows)
- **Cron Jobs** (Linux/macOS)

Example cron job (Linux/macOS) to run the script daily at 9 AM:

```bash
0 9 * * * /usr/bin/python3 /path-to-project/email_sender.py
```

---

## 📢 **Contributing**

Feel free to fork this repository and submit pull requests!

---

## 🛑 **Disclaimer**

- **Do NOT** use this script for spam or unsolicited emails.
- Ensure compliance with **Google, Outlook, or other SMTP provider policies**.
- **Use responsibly** to avoid your account being flagged.

---

## 📝 **License**

This project is licensed under the MIT License.

```python
MIT License

© 2022 Mishal KR
```

---

## 🧑‍💻 **Developer**

- **Mishal KR**