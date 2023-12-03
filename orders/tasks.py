from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_email_about_new_order(order_id, description, created, email):
    subject = f"New order #{order_id}"
    message = f"The order {description} {created}"

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=True,
    )


@shared_task
def send_email_about_assigned_master(meeting_time, recipient_email):
    subject = f"New status in your order"
    message = f"Master can help you order! Come to out office at the {meeting_time}"

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[recipient_email],
        fail_silently=True,
    )


@shared_task
def send_email_about_canceled_order(recipient_email):
    subject = f"Order status"
    message = f"We are sorry, but your email has a something wrong information"

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[recipient_email],
        fail_silently=True,
    )
