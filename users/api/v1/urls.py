from django.urls import path

from .views import UserRegistrationAPIView , VerifyEmailAPIView , ResendActivationAPIView

urlpatterns = [
    path('registration/' , UserRegistrationAPIView.as_view() , name='user-registration'),
    path('activation/', VerifyEmailAPIView.as_view(), name='user-activation'),
    path('resend-registration/', ResendActivationAPIView.as_view(), name='resend-user-registration'),
]