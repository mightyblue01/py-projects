import smtplib, ssl
from covid19_logger import logger

port = 465  # For SSL
smtp_server = "smtp.gmail.com"

def send_email(msgbody, sender_email, receivers_email_string):
    try:
        password = input("Type your password and press enter: ")
        logger.info('sender email {}'.format(sender_email))
        logger.info('receiver email {}'.format(receivers_email_string))
        receiver_email = receivers_email_string.split()

        SUBJECT = "Automatic email - latest Corona stats"
        message = 'Subject: {}\n\n{}'.format(SUBJECT, msgbody)

        logger.info('sending email now {}'.format(message))
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
    except Exception as e:
        logger.exception('Exception occured in send_email method {}'.format(e))