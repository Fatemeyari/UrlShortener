from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from .serializers import ShortUrlCreateSerializer

class ShortUrlCreateAPIView(CreateAPIView):
    serializer_class = ShortUrlCreateSerializer
    permission_classes = [IsAuthenticated]