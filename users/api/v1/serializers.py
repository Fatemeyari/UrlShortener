from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

from ...models import User , Profile

user=get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password1=serializers.CharField(label='Password1')
    class Meta:
        model=User
        fields=['phone_number' , 'email' , 'password' , 'password1']

    def validate(self, attrs):
        if attrs['password'] != attrs['password1']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    def create(self , validated_data):
        user = User(
            phone_number=validated_data['phone_number'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ResendActivationsSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return value


class UserLoginSerializer(serializers.Serializer):
    phone_number=serializers.CharField(max_length=13)
    password=serializers.CharField(label='Password')

    def validate(self , attrs):
        phone_number=attrs['phone_number']
        password=attrs['password']
        if phone_number and password:
            user=authenticate(phone_number=phone_number,password=password)
            if not user:
                raise serializers.ValidationError("Invalid phone number or password.")
            if not user.is_active:
                raise serializers.ValidationError("User account is not active.")
        else:
            raise serializers.ValidationError("Both phone number and password are required.")

        attrs["user"] = user
        return attrs



class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user is associated with this email.")
        return value

class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

class UserSerializer(serializers.Serializer):
    phone_number=serializers.CharField()
    email=serializers.EmailField()

class UserProfileSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model=Profile
        fields=['user' , 'full_name','avatar', 'bio' , 'website', 'is_premium']


class ChangeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'phone_number']


class ChangeUserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)

    class Meta:
        model = Profile
        fields = ['user', 'full_name', 'avatar', 'bio', 'website', 'is_premium']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        for attr, value in user_data.items():
            setattr(instance.user, attr, value)
        instance.user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
