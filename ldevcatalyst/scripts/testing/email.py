import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

email_host = 'mail.tn.gov.in'
email_port = 465
email_username = 'aso.itnt'
email_password = 'uheim}a3'
subject = 'You iTNT registration has been approved'
body = f'''
                        Username: test
                        Password: test
                        Login URL: https://itnthub.tn.gov.in/innovation-portal/dashboard
                        '''
message = MIMEMultipart()
message['From'] = 'aso.itnt@tn.gov.in'
message['To'] = 'pranaymadasi1@gmail.com'  
message['Subject'] = subject
message.attach(MIMEText(body, 'plain'))
with smtplib.SMTP_SSL(email_host, email_port) as server:
    server.login(email_username, email_password)
    print(server.sendmail('aso.itnt@tn.gov.in', ['pranaymadasi1@gmail.com'], message.as_string()))