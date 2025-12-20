from rest_framework import serializers

from ...short_code import generate_short_code , validate_short_url
from ...models import ShortURL

class ShortUrlCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=ShortURL
        fields=['original_url', 'custom_alias']


    def create(self, validated_data):
        user=self.context['request'].user
        if not user.profile.is_premium:
            user_links_count = ShortURL.objects.filter(user=user).count()
            if user_links_count >= 50:
                raise serializers.ValidationError(
                    "Non-premium users can only create up to 50 links."
                )
        custom_alias = validated_data.get('custom_alias')
        if custom_alias:
            validate_short_url(custom_alias)
            short_code = custom_alias

        else:
            short_code = generate_short_code()
        return ShortURL.objects.create(
            user=user,
            short_code=short_code,
            **validated_data
        )


class ShortUrlUpdateSerializer(serializers.ModelSerializer):
    class Meta:

        model=ShortURL
        fields=['is_active','qr_code','expires_time']


class ShortUrlListSerializer(serializers.ModelSerializer):
    class Meta:
        model=ShortURL
        fields = [
            'original_url', 'short_code', 'clicks', 'is_active',
            'custom_alias', 'qr_code', 'expires_time',
            'created_time', 'last_clicked'
        ]