from django.urls import path

from .views import ShortUrlCreateAPIView

urlpatterns = [
    path('shorten/', ShortUrlCreateAPIView.as_view(), name='shorten-url'),
]
