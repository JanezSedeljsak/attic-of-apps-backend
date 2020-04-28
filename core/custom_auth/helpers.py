import smtplib
from .models import *
from django.contrib.auth.models import User
import sys

gmail_user = 'brainjet.team@gmail.com'
gmail_password = 'ra-ff-admin'


class SendEmail:

    @staticmethod
    def confirm_acc(data):
        global gmail_user, gmail_password
        sent_from = gmail_user
        to = [data['user'].email]
        subject = 'Confirm your account!'
        body = f'Open link: {data["fallback"]}/login?uuid={data["uuid"]} to confirm your account'

        email_text = """\
        From: %s
        To: %s
        Subject: %s

        %s
        """ % (sent_from, ", ".join(to), subject, body)

        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(gmail_user, gmail_password)
            server.sendmail(sent_from, to, email_text)
            server.close()
        except:
            print("Unexpected error:", sys.exc_info()[0])
            return False

        return True

    @staticmethod
    def reset_pass(data):
        global gmail_user, gmail_password
        sent_from = gmail_user
        to = [data['user'].email]
        subject = 'Password reset!'
        body = f'Open link: {data["fallback"]}/forgot-pass/{data["uuid"]} to reset your password'

        email_text = """\
        From: %s
        To: %s
        Subject: %s

        %s
        """ % (sent_from, ", ".join(to), subject, body)

        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(gmail_user, gmail_password)
            server.sendmail(sent_from, to, email_text)
            server.close()
        except:
            print("Unexpected error:", sys.exc_info()[0])
            return False

        return True