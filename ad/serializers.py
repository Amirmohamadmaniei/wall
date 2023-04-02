from rest_framework import serializers
from .models import AD, Image
from django.utils import timezone


class ImageUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'
        extra_kwargs = {
            'ad': {'required': False}
        }


class ImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ('id', 'image')

    def get_image(self, obj):
        request = self.context.get('request')
        image_url = obj.image.url
        return request.build_absolute_uri(image_url)


class ADSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    user = serializers.SlugRelatedField(slug_field='email', read_only=True)

    class Meta:
        model = AD
        fields = '__all__'
        extra_kwargs = {
            'user': {'required': False}
        }

    def create(self, validated_data):
        request = self.context['request']
        validated_data['user'] = request.user
        ad = AD.objects.create(**validated_data)
        for v in request.FILES.values():
            Image.objects.create(ad=ad, image=v)
        return ad

    def get_images(self, obj):
        return ImageSerializer(instance=obj.images.all(), many=True, context={'request': self.context['request']}).data

    def get_date(self, obj):
        date = (timezone.now() - obj.created).seconds

        if date > 86400:
            return f'{date // 86400} days'
        elif date > 3600:
            return f'{date // 3600} hours'
        elif date > 60:
            return f'{date // 60} minutes'
        return f'{date // 60} seconds'
