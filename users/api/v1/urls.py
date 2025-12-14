from django.urls import path

from .views import (UserRegistrationAPIView , VerifyEmailAPIView , ResendActivationAPIView , ResendVerifyEmailAPIView,
                    UserLoginAPIView, LogoutAPIView)

urlpatterns = [
    path('registration/' , UserRegistrationAPIView.as_view() , name='user-registration'),
    path('activation/', VerifyEmailAPIView.as_view(), name='user-activation'),
    path('resend-registration/', ResendActivationAPIView.as_view(), name='resend-user-registration'),
    path('resend/activation/' ,ResendVerifyEmailAPIView.as_view() , name='resend-user-activation'),
    path('login/', UserLoginAPIView.as_view(), name='user-login'),
    path('logout/', LogoutAPIView.as_view(), name='auth_logout'),
]