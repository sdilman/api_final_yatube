from rest_framework import permissions


class AuthorOrReadOnly(permissions.BasePermission):
    """Разрешает только автору доступ к документу."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class ReadOnly(permissions.BasePermission):
    """Разрешает доступ к методам не изменяющим объект."""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
