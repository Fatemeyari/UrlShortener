from django.urls import path

from .views import UserRegistrationAPIView , VerifyEmailAPIView

urlpatterns = [
    #create-user
    path('registration/' , UserRegistrationAPIView.as_view() , name='user-registration'),
    path('activation/', VerifyEmailAPIView.as_view(), name='user-activation'),
]