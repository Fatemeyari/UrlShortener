from django.urls import path

from .views import UserRegistrationAPIView

urlpatterns = [
    #create-user
    path('register/' , UserRegistrationAPIView.as_view() , name='user-registration')
]