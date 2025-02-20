from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from posts.models import Comment, Follow, Group, Post


class RecordSerializer(serializers.ModelSerializer):
    """Serializer for model with author."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )


class PostSerializer(RecordSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(RecordSerializer):
    author = SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        fields = ('id', 'author', 'post', 'text', 'created')
        read_only_fields = ('post',)
        model = Comment


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    user = SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )
    following = SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        fields = ('user', 'following')
        read_only_fields = ('user',)
        model = Follow
