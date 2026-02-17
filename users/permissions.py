from rest_framework import permissions

class IsModer(permissions.BasePermission):
    """
    Проверяем пользователя, является ли он модератором.
    """

    message = 'У вас нет прав на это действие'

    def has_permission(self, request, view):
        return request.user.groups.filter(name='moders').exists()


class IsOwner(permissions.BasePermission):
    """
    Проверяем пользователя, является ли он владельцем.
    """

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False
