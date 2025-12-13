from django.core.mail import send_mail
from django.conf import settings

from rest_framework_simplejwt.tokens import AccessToken , RefreshToken

def store_email_verification_token(user):
    token = AccessToken.for_user(user)
    token["email_verify"] = True
    return str(token)


def send_verification_email(user):
    token = store_email_verification_token(user)
    verification_link = (
        f"http://localhost:8000/users/api/v1/activation/?token={token}"
    )

    send_mail(
        subject='Activate your account',
        message=f'Click this link to verify your email: {verification_link}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False
    )



def store_email_resend_varification_token(user):
    token=RefreshToken.for_user(user)
    token['resend_email_verify']=True
    return str(token)
