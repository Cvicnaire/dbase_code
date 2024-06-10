#!/usr/bin/python3
import cgitb
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

cgitb.enable()  # Enable detailed error reports for debugging

print("Content-Type: text/html")  # Send HTTP header
print()  # End of headers

# Email configuration
sender_email = "ylabpassreset@gmail.com"  # Replace with your sender email address
receiver_email = "astoicad@bu.edu"  # Replace with the receiver's email address
password = "dvxmmmbbrkfsgoxy"  # Replace with your email account password or app password

# Email server configuration
smtp_server = "smtp.example.com"  # Replace with your SMTP server
smtp_port = 587  # SMTP port number, often 587 for TLS or 465 for SSL

# Prepare the email message
message = MIMEMultipart()
message['From'] = sender_email
message['To'] = receiver_email
message['Subject'] = 'BEE MOVIE'
body = "Triple BAM"
message.attach(MIMEText(body, 'plain'))

# Sending the email
try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Start TLS encryption
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message.as_string())
    server.quit()
    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {str(e)}")
