from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions, viewsets
from rest_framework.exceptions import (
    AuthenticationFailed, NotFound, PermissionDenied
)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from posts.models import Comment, Follow, Group, Post
from .serializers import (
    CommentSerializer, GroupSerializer, FollowSerializer, PostSerializer
)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def check_user_is_post_author(self):
        """Проверить совпадение автора поста и текущего пользователя."""
        return self.get_object().author == self.request.user

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if not self.check_user_is_post_author():
            raise PermissionDenied('Пост другого автора нельзя редактировать.')
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        if not self.request.user.is_authenticated:
            raise AuthenticationFailed(
                'Анонимный пользователь не может удалять.'
            )
        if not self.check_user_is_post_author():
            raise PermissionDenied('Пост другого автора нельзя удалять.')
        super().perform_destroy(instance)

    # def destroy(self, request, *args, **kwargs):
    #     try:
    #         self.get_object()
    #     except Post.DoesNotExist:
    #         return Response(status=204)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def check_user_is_comment_author(self):
        """Проверить совпадение автора коментария и текущего пользователя."""
        return self.get_object().author == self.request.user

    def get_post_id(self):
        """Получить post_id если передан, или сгенерировать исключение."""
        post_id = self.kwargs.get('post_id')
        if post_id is None:
            # Не используем not post_id исключая возможность post_id == 0
            raise PermissionDenied("Параметр 'post_id' отсутствует.")
        return post_id

    def get_post(self):
        """Получить post если существует, или сгенерировать исключение."""
        return get_object_or_404(Post, pk=self.get_post_id())

    def get_queryset(self):
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())

    def perform_update(self, serializer):
        if not self.check_user_is_comment_author():
            raise PermissionDenied('Пост другого автора нельзя редактировать.')
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        if not self.check_user_is_comment_author():
            raise PermissionDenied('Пост другого автора нельзя удалять.')
        super().perform_destroy(instance)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class FollowViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        """Вернуть подписки пользователя сделавшего запрос."""
        user = self.request.user
        return Follow.objects.filter(user=user)

    def perform_create(self, serializer):
        """Подписать текущего пользователя на пользователя из запроса."""
        if self.get_object().following == self.request.user:
            raise PermissionDenied('Пост другого автора нельзя удалять.')
        serializer.save(user=self.request.user)
