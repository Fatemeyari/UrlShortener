from rest_framework import serializers

from ...short_code import generate_short_code , validate_short_url
from ...models import ShortURL

class ShortUrlCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=ShortURL
        fields=['original_url', 'custom_alias']


    def create(self, validated_data):
        user=self.context['request'].user
        custom_alias = validated_data.get('custom_alias' , None)
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