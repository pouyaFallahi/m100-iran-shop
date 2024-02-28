from config import settings
from celery import shared_task
from django.core import signing
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _


@shared_task
def send_verification_email(email, verification_code):
    mail_subject = _('Confirmation Email from Your Website')
    message = f'Your verification code is: {verification_code}'
    send_mail(
        subject=mail_subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )


@shared_task
def send_email_for_change_password(email, reset_link):
    print(f'start {email} and link:\n{reset_link}')
    send_mail(
        subject=_('Password Reset'),
        message=_(f'Use the following link to reset your password: {reset_link}'),
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )
    print('end')