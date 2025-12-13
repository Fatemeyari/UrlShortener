from rest_framework import serializers

from ...models import User


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



