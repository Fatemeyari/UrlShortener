from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated


from .serializers import ShortUrlCreateSerializer , ShortUrlUpdateSerializer , ShortUrlListSerializer
from ...models import ShortURL


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
