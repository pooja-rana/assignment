from django.urls import reverse
from accounts.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import smart_bytes
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.core.mail import send_mail


def email_send(subject, message, from_email, to_list, html_message):
    """ Email send for comnfirmation and password reset """
    print('Request get for send Email')
    send_mail(subject, message, from_email, to_list, html_message=html_message, fail_silently=False)
    print('Mail send Successfull.')


class PasswordReset:
    """Send Email to User for email id verification"""

    @classmethod
    def send_password_reset_email(cls, redirect_url, current_site, user_id):
        user = User.objects.get(pk=user_id)
        uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)

        relativeLink = reverse("accounts:password-reset-confirm", kwargs={"uidb64": uidb64, "token": token})

        absurl = "http://" + current_site + relativeLink

        domain = absurl + "?redirect_url=" + redirect_url

        html_message = render_to_string('registration/password_reset_email.html', {
            "domain": domain,
            "uid": uidb64,
            "token": token,
            "user": user
        })

        message = strip_tags(html_message)

        from_email = settings.EMAIL_HOST_USER
        subject = "Reset Your Password"
        to_list = [user.email]

        send_email = email_send(subject, message, from_email, to_list, html_message)
        return send_email