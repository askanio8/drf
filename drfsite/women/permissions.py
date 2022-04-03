from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:  # SAFE_METHODS это GET, HEAD, OPTIONS
            return True

        return bool(request.user and request.user.is_staff)  # если это администратор


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user  # если изменить пытаестся тот, кто создал запись
