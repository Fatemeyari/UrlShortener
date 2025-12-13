from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status

from rest_framework_simplejwt.tokens import AccessToken , RefreshToken
from django.contrib.auth import get_user_model

from .serializers import UserRegistrationSerializer , ResendActivationsSerializer
from ...utils import send_verification_email , resend_varification_email

User = get_user_model()

class UserRegistrationAPIView(generics.GenericAPIView):
    serializer_class=UserRegistrationSerializer
    def post(self, request):
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_verification_email(user)
            return Response({

                   "message" :"Activation link has been sent to your email"

                }
                    ,status=status.HTTP_201_CREATED
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailAPIView(APIView):
    def get(self, request):
        token = request.query_params.get('token')

        if not token:
            return Response({"detail": "Token missing"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            payload = AccessToken(token)

            if not payload.get("email_verify"):
                return Response({"detail": "Invalid verification token"},status=status.HTTP_400_BAD_REQUEST)

            user_id = payload["user_id"]
            user = User.objects.get(id=user_id)

            if user.is_active:
                return Response({"message": "Account already activated"},status=status.HTTP_200_OK)

            user.is_active = True
            user.save(update_fields=["is_active"])

            return Response({"message": "Email verified successfully"},status=status.HTTP_200_OK)

        except Exception as e:
            return Response( {"detail": "Invalid or expired token"},status=status.HTTP_400_BAD_REQUEST)

class ResendActivationAPIView(generics.GenericAPIView):
    serializer_class = ResendActivationsSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")
        user = User.objects.filter(email=email).first()

        if not user:
            return Response({"detail": "User with this email does not exist."}, status=400)

        if user.is_active:
            return Response({"message": "Account already activated"}, status=200)

        resend_varification_email(user)
        return Response({
            "message": "Activation link has been resent to your email"
        }, status=201)


class ResendVerifyEmailAPIView(APIView):
    def get(self, request):
        token = request.query_params.get('token')
        if not token:
            return Response({"detail": "Token missing"}, status=400)

        try:
            payload = RefreshToken(token)

            if not payload.get("resend_email_verify"):
                return Response({"detail": "Invalid token"}, status=400)

            user_id = payload["user_id"]
            user = User.objects.get(id=user_id)

            if user.is_active:
                return Response({"message": "Account already activated"}, status=200)

            user.is_active = True
            user.save(update_fields=["is_active"])

            return Response({"message": "Email verified successfully"}, status=200)

        except Exception as e:
            return Response({"detail": "Invalid or expired token"}, status=400)
