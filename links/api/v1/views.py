from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404 , redirect
from django.utils import timezone
from django.core.files.base import ContentFile

import redis
from .serializers import ShortUrlCreateSerializer , ShortUrlUpdateSerializer , ShortUrlListSerializer
from ...models import ShortURL,ClickStats
import qrcode
from io import BytesIO

r = redis.Redis(host='localhost', port=6379, db=0)

def generate_qr_code(link):
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5
    )
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    filename = f"{link}.png"
    filebuffer = ContentFile(buffer.getvalue())
    return filename, filebuffer

class ShortUrlCreateAPIView(CreateAPIView):
    serializer_class = ShortUrlCreateSerializer
    permission_classes = [IsAuthenticated]


class ShortUrlUpdatedAPIView(UpdateAPIView):
    serializer_class = ShortUrlUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ShortURL.objects.filter(user=self.request.user)


class ShortUrlDeleteAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return ShortURL.objects.filter(user=self.request.user)


class ShortUrlListAPIView(ListAPIView):
    serializer_class = ShortUrlListSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return ShortURL.objects.filter(user=self.request.user)

class ShortURLRedirectAPIView(APIView):

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')

    def get(self, request, short_code, format=None):
        link = None
        original_url = r.get(short_code)
        if original_url:
            original_url = original_url.decode('utf-8')
            link = get_object_or_404(ShortURL, short_code=short_code, is_active=True)
        else:
            link = get_object_or_404(ShortURL, short_code=short_code, is_active=True)
            original_url = link.original_url
            r.set(short_code, original_url, ex=3600)

        ip_address = self.get_client_ip(request) 
        browser = request.META.get('HTTP_USER_AGENT', 'unknown')

        ClickStats.objects.create(
            short_url=link,
            ip_address=ip_address,
            browser=browser,
            timestamp=timezone.now()
        )

        link.clicks += 1
        link.last_clicked = timezone.now()
        link.save(update_fields=['clicks', 'last_clicked'])

        return redirect(original_url)
