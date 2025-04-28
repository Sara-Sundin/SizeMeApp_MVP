from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def send_order_confirmation_email(order):
    context = {
        'order': order,
        'order_items': order.lineitems.all(),
        'contact_email': settings.DEFAULT_FROM_EMAIL,
    }
    
    subject = render_to_string('checkout/confirmation_emails/confirmation_email_subject.txt', context).strip()
    body = render_to_string('checkout/confirmation_emails/confirmation_email_body.txt', context)
    
    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [order.email],
        fail_silently=False,
    )
