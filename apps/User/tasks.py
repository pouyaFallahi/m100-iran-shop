from config import settings
from celery import shared_task
from django.core import signing
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _



@shared_task
def send_verification_email(email, verification_code):
    print('first')
    mail_subject = _('Confirmation Email from Your Website')
    message = f'Your verification code is: {verification_code}'
    send_mail(
        subject=mail_subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )
    print('end')


@shared_task
def send_email_for_change_password(email):
    sing = signing.Signer()
    mail = sing.sign(email)
    print(mail, type(mail))
    url = 'http://127.0.0.1:8000/' + mail.value + '/'
    mail_subject = _('Request to change password')
    message = _(f'link to change: {url}')
    send_mail(
        subject=mail_subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )

