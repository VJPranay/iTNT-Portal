from ldevcatalyst import settings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

email_host = settings.email_host
email_port = settings.email_port
email_username = settings.email_username
email_from = settings.email_from
email_password = settings.email_password
email_from = settings.email_from
email_to = ['pranaymadasi1@gmail.com','pranay@ldev.in']

                # Email content
subject = 'New Support Request'
body = f'''
                        Name: name
                        email: email
                        mobile: mobile
                        Account Role: account_role
                        Support Category: support_category
                        Short Description: short_description
                        '''
                # Constructing email message
message = MIMEMultipart()
message['From'] = email_from
message['Subject'] = subject
message.attach(MIMEText(body, 'plain'))

                # Send email
with smtplib.SMTP_SSL(email_host, email_port) as server:
    server.login(email_username, email_password)
    server.sendmail(email_from, email_to, message.as_string())