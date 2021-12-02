from rest_framework import serializers
from like import services as likes_services
from .models import *


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Post
        fields = ('id', 'title', 'description','total_likes', 'author',)

    def create(self, validated_data):
        request = self.context.get('request')
        pictures_files = request.FILES
        post = Post.objects.create(
            author=request.user,
            **validated_data
        )
        return post

    def update(self, instance, validated_data):
        request = self.context.get('request')
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.pictures.all().delete()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation

    def get_is_fan(self, obj):
        """
        Проверяет, лайкнул ли `request.user` продукт (`obj`).
        """
        user = self.context.get('request').user
        return likes_services.is_fan(obj, user)
