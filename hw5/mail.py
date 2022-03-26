import argparse
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def SmtpSend(recipients, sender, subject, data, smtpServer, smtpPort, smtpPassword, data_type):
    smtpObj = smtplib.SMTP(smtpServer, 587)
    smtpObj.starttls()
    smtpObj.login(sender, smtpPassword)
    message = MIMEMultipart('alternative')
    message['Subject'] = "Hello!"
    message['From'] = sender
    message['To'] = recipients
    if data_type == 'html':
        message.attach(MIMEText(data, "html"))
    elif data_type == 'txt':
        message.attach(MIMEText(data, "plain"))
    else:
        message.attach(MIMEText('ERROR this user send you a file with incorrect extencion', "plain"))
    smtpObj.sendmail(sender, recipients, message.as_string())
    smtpObj.quit()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('sender', type=str)
    parser.add_argument('password', type=str)
    parser.add_argument('recipients', type=str)
    parser.add_argument('file_name', type=str)
    args = parser.parse_args()
    f = open(args.file_name)
    message = f.read()
    SmtpSend(
        recipients=args.recipients,
        sender=args.sender,
        subject="Test subject", 
        data=message,
        smtpServer="smtp.gmail.com",
        smtpPort=25,
        smtpPassword=args.password,
        data_type = args.file_name.split('.')[-1]
    )

if __name__ == '__main__':
    main()
