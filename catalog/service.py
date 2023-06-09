from django.conf import settings
from django.core.mail import send_mail


def send_email():
    send_mail(
        'Поздравляем',
        'Статья набрала сто просмотров',
        settings.EMAIL_HOST_USER,
        ['maxloginov2001@mail.ru'],
    )