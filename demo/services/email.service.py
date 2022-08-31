from django.core.mail import EmailMessage


class EmailSend:
    """sending email formate for all email sender"""

    @classmethod
    def send_email(cls, subject, message, to_email):

        email = EmailMessage(subject, message, to=to_email)
        send_email = email.send()
        return send_email