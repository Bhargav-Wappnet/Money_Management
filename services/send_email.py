from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model


@shared_task
def send_activation_link_email(user_id):
    # Retrieve the User object
    User = get_user_model()
    user = User.objects.get(pk=user_id)

    email_subject = f"Activation link for {user}"
    email_body = render_to_string("activation.html", {"user": user})
    email = EmailMessage(email_subject, email_body, to=[user.email])
    email.content_subtype = "html"
    email.send()


@shared_task
def send_forget_password_email(user_id):
    # Retrieve the User object
    User = get_user_model()
    user = User.objects.get(pk=user_id)

    email_subject = f"Reset Password Link {user}"
    email_body = render_to_string("forget_pass.html", {"user": user})
    email = EmailMessage(email_subject, email_body, to=[user.email])
    email.content_subtype = "html"
    email.send()
