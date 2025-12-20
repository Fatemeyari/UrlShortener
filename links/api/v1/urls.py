from django.urls import path

from .views import ShortUrlCreateAPIView , ShortUrlUpdatedAPIView

urlpatterns = [
    path('create-url/', ShortUrlCreateAPIView.as_view(), name='create-url'),
    path('edit-url/<int:pk>/' ,ShortUrlUpdatedAPIView.as_view() , name='edit-url' ),
]
