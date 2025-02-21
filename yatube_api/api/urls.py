from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    CommentViewSet,
    FollowViewSet,
    GroupViewSet,
    PostViewSet
)


router = DefaultRouter()
router.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)
router.register('groups', GroupViewSet)
router.register('follow', FollowViewSet)
router.register('posts', PostViewSet)


version_patterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
    path('', include(router.urls))
]

urlpatterns = [
    path('v1/', include(version_patterns))
]
