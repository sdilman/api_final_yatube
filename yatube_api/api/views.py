from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import LimitOffsetPagination

from posts.models import Follow, Group, Post
from .permissions import AuthorOrReadOnly
from .serializers import (
    CommentSerializer, GroupSerializer, FollowSerializer, PostSerializer
)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (AuthorOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    permission_classes = (AuthorOrReadOnly,)

    def get_post_id(self):
        """Получить post_id если передан, или сгенерировать исключение."""
        post_id = self.kwargs.get('post_id')
        if post_id is None:
            raise PermissionDenied('Параметр post_id отсутствует.')
        return post_id

    def get_post(self):
        """Получить post если существует, или сгенерировать исключение."""
        return get_object_or_404(Post, pk=self.get_post_id())

    def get_queryset(self):
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.AllowAny,)


class FollowViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        """Вернуть подписки пользователя сделавшего запрос."""
        return self.request.user.subscriptions.all()

    def perform_create(self, serializer):
        """Подписать текущего пользователя на пользователя из запроса."""
        serializer.save(user=self.request.user)
