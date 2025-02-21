from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from .exceptions import SerializerInitializationException
from posts.models import Comment, Follow, Group, Post


class RecordSerializer(serializers.ModelSerializer):
    """Serializer for model with author."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )


class CommentSerializer(RecordSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')
        read_only_fields = ('post',)

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            author = request.user
        else:
            raise SerializerInitializationException('context не установлен.')
        validated_data['author'] = author
        return super().create(validated_data)


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class PostSerializer(RecordSerializer):

    class Meta:
        model = Post
        fields = ('id', 'text', 'pub_date', 'author', 'image', 'group')


class FollowSerializer(serializers.ModelSerializer):
    user = SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    following = SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        fields = ('user', 'following')
        read_only_fields = ('user',)
        model = Follow
