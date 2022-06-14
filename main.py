"""
This script will send an email with attachments, it is mainly used to send logs
from a remote host back to a local host, so it can be stored for invesgation.
"""
import smtplib
import argparse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

# Get timestamp to include in the email subject.
now = datetime.now()
dt_string = now.strftime("%y/%m/%d %H:%M:%S")

# Parse commandline options
parser = argparse.ArgumentParser(prog="send_email")
parser.add_argument("--sender", type=str, required=True, help="Sender email address")
parser.add_argument("--receiver", type=str, required=True, help="Receiver email address")
parser.add_argument("--file", type=str, help="File to send (if any).")
args = parser.parse_args()

# Declare email related variables
smtp_ssl_host = "smtp.gmail.com"
smtp_ssl_port = 465
subject = "Log reports " + dt_string
body = "This is an automated email report, attached the available logs, if any."
password = input("Enter your email password: ") # Not safe, meant for presentation.
sender = args.sender
receiver = args.receiver
attachment_file = args.file

# Setup the MIME
message = MIMEMultipart()
message["From"] = sender
message["To"] = receiver
message["Subject"] = subject
message.attach(MIMEText(body, "plain"))

#Attach the file
if attachment_file is not None:
    binary_file = open(attachment_file, "rb")

    payload = MIMEBase("application", "octate-stream", Name=attachment_file)
    payload.set_payload((binary_file).read())

    encoders.encode_base64(payload)

    payload.add_header("Content-Decomposition", "attachment", filename=attachment_file)
    message.attach(payload)

# Initialize SMTP session and send email
session = smtplib.SMTP(smtp_ssl_host, smtp_ssl_port)
session.starttls()

session.login(sender, password)
session.sendmail(sender, receiver, message.as_string())
session.quit()

print(f"Mail sent to {receiver} with subject: {subject}")
