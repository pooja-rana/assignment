from celery import Task
from assignment_project.demo.services.password_reset_email_services import PasswordReset
from assignment_project.assignment_project.celery import app


class SendPasswordResetEmail(Task):
    """Task for password reset email send with celery"""

    name = "send_password_reset_email"

    def run(self, redirect_url, current_site, user_id):
        try:
            PasswordReset.send_password_reset_email(redirect_url, current_site, user_id)
        except Exception as e:
            print(e)


send_password_reset_email = app.register_task(SendPasswordResetEmail())