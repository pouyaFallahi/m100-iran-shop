from celery import shared_task
from django.core.mail import send_mail
from config import settings
from django.utils.translation import gettext_lazy as _


@shared_task(bind=True)
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


