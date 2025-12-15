from django.urls import path

from .views import (UserRegistrationAPIView , VerifyEmailAPIView , ResendActivationAPIView , ResendVerifyEmailAPIView,
                    UserLoginAPIView, LogoutAPIView, PasswordResetConfirmAPIView , PasswordResetRequestAPIView,
                ShowUserProfile,ChangeUserProfileAPIView)

urlpatterns = [
    path('registration/' , UserRegistrationAPIView.as_view() , name='user-registration'),
    path('activation/', VerifyEmailAPIView.as_view(), name='user-activation'),
    path('resend-registration/', ResendActivationAPIView.as_view(), name='resend-user-registration'),
    path('resend/activation/' ,ResendVerifyEmailAPIView.as_view() , name='resend-user-activation'),
    path('reset-password/', PasswordResetRequestAPIView.as_view(), name='password-reset-request'),
    path('reset-password/confirm/', PasswordResetConfirmAPIView.as_view(), name='password-reset-confirm'),
    path('login/', UserLoginAPIView.as_view(), name='user-login'),
    path('logout/', LogoutAPIView.as_view(), name='auth_logout'),
    path('profile/' ,ShowUserProfile.as_view() , name='user-profile'),
    path('profile/change/', ChangeUserProfileAPIView.as_view(), name='user-profile'),
]