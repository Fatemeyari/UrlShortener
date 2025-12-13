from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status

from .serializers import UserRegistrationSerializer

class UserRegistrationAPIView(generics.GenericAPIView):
    serializer_class=UserRegistrationSerializer
    def post(self, request):
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
               "message" :"Activation link has been sent to your email"

            }
                ,status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

