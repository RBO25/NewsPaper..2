from django.db.models.signals import m2m_changed
from django.dispatch import receiver # импортируем нужный декоратор
from django.core.mail import EmailMultiAlternatives
from .models import Category
from django.template.loader import render_to_string
from django.conf import settings


def send_notifications(preview, pk, title, subscribers):
    html_context = render_to_string(
        'mail.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}',
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFOULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()

# создаём функцию-обработчик с параметрами под регистрацию сигнала
@receiver(m2m_changed, sender=Category)
def notify_about_new_post(sender, instance, created, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        subscribers: list[str] = []
        for category in categories:
            subscribers += category.subscribers.all()

        subscribers = [s.mail for s in subscribers]

        send_notifications(instance.preview(), instance.id, instance.title, subscribers)