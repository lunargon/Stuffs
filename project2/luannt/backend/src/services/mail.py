import ssl
import smtplib
from email.message import EmailMessage
from src.utils import MAIL_FROM, MAIL_SERVER, MAIL_PASSWORD

# Class to send mail
class Mailsender():
    # send otp to mail
    def send_otp(self, subject: str, email_to: str, otp: str):
        try:
            em = EmailMessage()
            em['From'] = MAIL_FROM
            em['To'] = email_to
            em['Subject'] = subject
            body = f"""Here is your otp to activate your account: {otp}"""
            em.set_content(body)

            context = ssl.create_default_context()

            with smtplib.SMTP_SSL(MAIL_SERVER, 465, context=context) as smtp:
                smtp.login(MAIL_FROM, MAIL_PASSWORD)
                smtp.sendmail(MAIL_FROM, email_to, em.as_string())
        except Exception as e:
            raise Exception(str(e), exc_info=True) from e