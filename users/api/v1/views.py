from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated , IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.tokens import AccessToken , RefreshToken , TokenError

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from .serializers import (UserRegistrationSerializer , ResendActivationsSerializer , UserLoginSerializer ,
                          PasswordResetRequestSerializer ,PasswordResetConfirmSerializer, UserProfileSerializer)
from ...utils import send_verification_email , resend_varification_email , send_password_reset_email
from ...models import Profile

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
            return Response({"detail": "User with this email does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        if user.is_active:
            return Response({"message": "Account already activated"}, status=status.HTTP_200_OK)

        resend_varification_email(user)
        return Response({
            "message": "Activation link has been resent to your email"
        }, status=201)


class ResendVerifyEmailAPIView(APIView):
    def get(self, request):
        token = request.query_params.get('token')
        if not token:
            return Response({"detail": "Token missing"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            payload = RefreshToken(token)

            if not payload.get("resend_email_verify"):
                return Response({"detail": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

            user_id = payload["user_id"]
            user = User.objects.get(id=user_id)

            if user.is_active:
                return Response({"message": "Account already activated"}, status=status.HTTP_200_OK)

            user.is_active = True
            user.save(update_fields=["is_active"])

            return Response({"message": "Email verified successfully"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"detail": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)

class UserLoginAPIView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    def post(self , request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data.get("user")
        refresh = RefreshToken.for_user(user)
        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }

        return Response({
            "message": "Login successful",
            "tokens": data
        }, status=status.HTTP_200_OK)

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"detail": "Refresh token is required."},status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            return Response({"detail": "Invalid or expired refresh token"}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestAPIView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = User.objects.get(email=email)
        send_password_reset_email(user)
        return Response({"message": "Password reset link has been sent to your email."}, status=status.HTTP_200_OK)


class PasswordResetConfirmAPIView(APIView):
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request):
        token = request.query_params.get('token')
        if not token:
            return Response({"detail": "Token missing."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            payload = AccessToken(token)
            if not payload.get('reset_password'):
                return Response({"detail": "Invalid reset token."}, status=status.HTTP_400_BAD_REQUEST)
            user_id = payload['user_id']
            user = User.objects.get(id=user_id)
        except Exception:
            return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)

class ShowUserProfile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = request.user.profile
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
