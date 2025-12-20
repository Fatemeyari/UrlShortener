from django.urls import path

from .views import ShortUrlCreateAPIView , ShortUrlUpdatedAPIView,ShortUrlDeleteAPIView,ShortUrlListAPIView

urlpatterns = [
    path('create-url/', ShortUrlCreateAPIView.as_view(), name='create-url'),
    path('edit-url/<int:pk>/' ,ShortUrlUpdatedAPIView.as_view() , name='edit-url' ),
    path('delete-url/<int:pk>/' ,ShortUrlDeleteAPIView.as_view(), name='delete-url' ),
    path('list-url/',ShortUrlListAPIView.as_view(), name='list-url'),
]
