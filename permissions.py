from rest_framework.permissions import BasePermission, SAFE_METHODS


class NotAuthenticated(BasePermission):
    message = 'permission denied , you are is authenticated , you must not authenticate'

    def has_permission(self, request, view):
        return not request.user.is_authenticated


class IsOwner(BasePermission):
    message = 'you can not update or Delete this AD'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user


class IsOwnerImage(BasePermission):
    message = 'you can not update or Delete this Image'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.ad.user == request.user
